package nexus.omega.r21r1.astranav

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.GnssStatus
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Build
import android.os.SystemClock
import java.time.Instant

/**
 * NEXUS OMEGA - R21R1 - WP-G2 - AstraNav GNSS companion reference (GPS_PROVIDER only).
 *
 * C1_DESCRIPTIVE_ONLY. Reference module for the nexus-nav-fix/v1 data contract
 * (schema/r21/r21r1/nexus-nav-fix-v1.schema.json; validator:
 * examples/r21/r21r1/nexus-nav-fix.mjs).
 *
 * Physical truth boundary:
 * - Uses LocationManager.GPS_PROVIDER only. Never the fused provider and never
 *   browser geolocation; such sources must fail closed downstream.
 * - A structurally valid fix is SOURCE_REPORTED_GNSS. The stronger class
 *   OFFLINE_NETWORK_DISABLED_TEST_VERIFIED additionally requires a witnessed physical
 *   test with airplane mode on and Wi-Fi and cell data off, recorded by the authorized
 *   operator lane. It is never set automatically by this module.
 * - Privacy: precise coordinates remain device-local (device_local_private=true).
 *   This module transmits nothing.
 *
 * Build status: STATIC_OR_BUILD_VALIDATED_NOT_HARDWARE_TESTED. This reference was not
 * executed on physical Pixel/Oppo hardware in the R21R1 MISTRAL lane.
 */
class AstraNavGnssCompanion(private val context: Context) {

    private val locationManager: LocationManager
        get() = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager

    private var satellitesVisible = 0
    private var satellitesUsedInFix = 0
    private var activeListener: LocationListener? = null

    /** Fine location permission is a hard precondition; without it no fix is valid. */
    fun hasFineLocationPermission(): Boolean =
        context.checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED

    /** The device must actually expose GPS_PROVIDER; absence is a fail-closed gap. */
    fun isGnssHardwarePresent(): Boolean =
        locationManager.allProviders.contains(LocationManager.GPS_PROVIDER)

    private val gnssStatusCallback = object : GnssStatus.Callback() {
        override fun onSatelliteStatusChanged(status: GnssStatus) {
            satellitesVisible = status.satelliteCount
            var used = 0
            for (index in 0 until status.satelliteCount) {
                if (status.usedInFix(index)) used++
            }
            satellitesUsedInFix = used
        }
    }

    /**
     * Register GPS_PROVIDER updates. Each Location is converted into the field set of
     * nexus-nav-fix/v1. isMock is only trustworthy on API 31 and above; on older
     * versions the validator must treat mock detection as unavailable, not as passed.
     */
    fun requestGpsFixes(onFix: (Map<String, Any?>) -> Unit) {
        require(hasFineLocationPermission()) {
            "ACCESS_FINE_LOCATION not granted; no GNSS fix is valid."
        }
        require(isGnssHardwarePresent()) {
            "GPS_PROVIDER not present; fail-closed, no fallback provider."
        }
        @Suppress("DEPRECATION")
        locationManager.registerGnssStatusCallback(gnssStatusCallback)
        val listener = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                if (location.provider != LocationManager.GPS_PROVIDER) return
                onFix(
                    mapOf(
                        "provider" to LocationManager.GPS_PROVIDER,
                        "latitude" to location.latitude,
                        "longitude" to location.longitude,
                        "altitude_m" to if (location.hasAltitude()) location.altitude else null,
                        "horizontal_accuracy_m" to location.accuracy.toDouble(),
                        "utc" to Instant.ofEpochMilli(location.time).toString(),
                        "elapsed_realtime_nanos" to location.elapsedRealtimeNanos,
                        "is_mock" to if (Build.VERSION.SDK_INT >= 31) location.isMock else false,
                        "satellites_visible" to satellitesVisible,
                        "satellites_used_in_fix" to satellitesUsedInFix,
                        "assistance_class" to "ASSISTANCE_UNKNOWN"
                    )
                )
            }
        }
        activeListener = listener
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000L, 0f, listener)
    }

    fun stop() {
        @Suppress("DEPRECATION")
        locationManager.unregisterGnssStatusCallback(gnssStatusCallback)
        activeListener?.let { locationManager.removeUpdates(it) }
        activeListener = null
    }
}
