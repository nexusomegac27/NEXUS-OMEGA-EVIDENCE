/* NEXUS OMEGA · BODYTWIN LIVE PANEL ISOLATED LAYOUT HOTFIX R0
 * C1_DESCRIPTIVE_ONLY. Does not inspect, modify or poll feed content.
 * Moves existing status panel outside <main> so it cannot participate
 * in the 4D viewer's internal grid/flex/positioning context.
 */
(() => {
  'use strict';
  const ID = 'nexus-bodytwin-live-c1';
  const ROOT = document.documentElement;
  let settled = false;
  let observer = null;
  const close = () => { if (observer) observer.disconnect(); observer = null; };
  function repair() {
    if (settled) return true;
    const matches = document.querySelectorAll('#' + ID);
    if (matches.length > 1) {
      ROOT.dataset.nexusBodytwinLayout = 'HOLD_DUPLICATE_PANEL';
      settled = true;
      close();
      return true;
    }
    if (matches.length === 0) return false;
    const panel = matches[0];
    const main = document.querySelector('main');
    const destination = (main && main.parentNode) || document.body;
    if (!destination) return false;
    const footer = !main && Array.from(destination.children).find(x => x.tagName === 'FOOTER');
    const before = main ? main.nextSibling : (footer || null);
    const alreadyPlaced = main
      ? panel.parentNode === destination && main.nextSibling === panel
      : panel.parentNode === destination && panel.nextSibling === before;
    if (!alreadyPlaced) destination.insertBefore(panel, before);
    panel.dataset.layoutFix = 'isolated';
    ROOT.dataset.nexusBodytwinLayout = 'PASS_ISOLATED_PANEL';
    settled = true;
    close();
    return true;
  }
  if (!repair()) {
    observer = new MutationObserver(() => { repair(); });
    observer.observe(document.documentElement, {childList: true, subtree: true});
    document.addEventListener('DOMContentLoaded', repair, {once: true});
    window.addEventListener('load', () => {
      if (!repair()) ROOT.dataset.nexusBodytwinLayout = 'HOLD_PANEL_NOT_FOUND';
    }, {once: true});
  }
})();
