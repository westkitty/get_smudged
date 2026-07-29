// ==UserScript==
// @name         Get Smudged - Random Poster Characters
// @namespace    https://github.com/westkitty/get_smudged
// @version      2.1.0
// @description  Picks a fresh random Smudge whenever a Jellyfin poster is entered, with a 1-in-1000 Dexter cameo.
// @match        https://media.westcat.ca/*
// @run-at       document-end
// @grant        none
// ==/UserScript==

(() => {
  'use strict';

  if (window.__getSmudgedRandomizerInstalled) return;
  window.__getSmudgedRandomizerInstalled = true;

  const CDN = 'https://cdn.jsdelivr.net/gh/westkitty/get_smudged@main/assets';
  const DEXTER_ODDS = 1000; // One Dexter appearance per 1,000 card entries on average.

  const SMUDGES = [
    'smudge-01-hyper-pounce.webp',
    'smudge-02-speed-walk.webp',
    'smudge-03-startled-dance.webp',
    'smudge-04-tall-sit.webp',
    'smudge-05-puffed-stand.webp',
    'smudge-06-wide-eyed-sit.webp',
    'smudge-07-low-stalk.webp',
    'smudge-08-goblin-claw.webp',
    'smudge-09-vertical-grab.webp',
    'smudge-10-full-sprint.webp',
    'smudge-11-whirlwind.webp',
    'smudge-12-upside-down-flail.webp',
    'smudge-13-low-pounce.webp',
    'smudge-14-boxing-stance.webp',
    'smudge-15-grumpy-loaf.webp',
    'smudge-16-sideways-startle.webp',
    'smudge-17-puffball-crouch.webp',
    'smudge-18-belly-roll.webp',
    'smudge-19-alert-stand.webp',
    'smudge-20-long-stretch.webp',
    'smudge-21-tornado-spin.webp',
    'smudge-22-slide-pounce.webp',
    'smudge-23-upside-down-drop.webp',
    'smudge-24-meerkat-stand.webp',
    'smudge-25-judgment-loaf.webp',
    'smudge-26-arched-side-eye.webp',
    'smudge-27-sneak-crawl.webp',
    'smudge-28-chaos-roll.webp',
    'smudge-29-bristled-stand.webp',
    'smudge-30-downward-stretch.webp'
  ];

  const DEXTER = `${CDN}/dexter/dexter-unimpressed.webp`;

  const injectCompatibilityStyles = () => {
    if (document.getElementById('getSmudgedRandomizerStyles')) return;

    const style = document.createElement('style');
    style.id = 'getSmudgedRandomizerStyles';
    style.textContent = `
      .card[data-smudge-randomized="true"]:is(:hover, :focus-within, :focus-visible)::after {
        background-image: var(--smudge-hover-image) !important;
        background-position: center !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        left: var(--smudge-hover-left, auto) !important;
        right: var(--smudge-hover-right, -24px) !important;
        bottom: var(--smudge-hover-bottom, 12px) !important;
        width: var(--smudge-active-size, 118px) !important;
        height: var(--smudge-active-size, 118px) !important;
        transform: rotate(var(--smudge-hover-rotation, -5deg)) !important;
      }

      .card[data-smudge-character="dexter"]:is(:hover, :focus-within, :focus-visible)::after {
        opacity: .96 !important;
        filter: drop-shadow(0 5px 8px rgba(0,0,0,.20)) !important;
      }
    `;
    document.documentElement.appendChild(style);
  };

  const randomInt = (max) => {
    if (max <= 0) return 0;
    if (window.crypto?.getRandomValues) {
      const values = new Uint32Array(1);
      window.crypto.getRandomValues(values);
      return values[0] % max;
    }
    return Math.floor(Math.random() * max);
  };

  const setPlacement = (card) => {
    const leftSide = randomInt(2) === 0;
    const rotation = randomInt(17) - 8;
    const bottom = 6 + randomInt(19);
    const size = 102 + randomInt(31);

    card.style.setProperty('--smudge-hover-left', leftSide ? '-22px' : 'auto');
    card.style.setProperty('--smudge-hover-right', leftSide ? 'auto' : '-24px');
    card.style.setProperty('--smudge-hover-bottom', `${bottom}px`);
    card.style.setProperty('--smudge-hover-rotation', `${rotation}deg`);
    card.style.setProperty('--smudge-active-size', `${size}px`);
  };

  const assignCharacter = (card) => {
    if (!(card instanceof HTMLElement)) return;

    card.dataset.smudgeRandomized = 'true';
    const isDexter = randomInt(DEXTER_ODDS) === 0;

    if (isDexter) {
      card.dataset.smudgeCharacter = 'dexter';
      card.style.setProperty('--smudge-hover-image', `url("${DEXTER}")`);
      card.style.setProperty('--smudge-active-size', '86px');
      card.style.setProperty('--smudge-hover-left', '-12px');
      card.style.setProperty('--smudge-hover-right', 'auto');
      card.style.setProperty('--smudge-hover-bottom', '8px');
      card.style.setProperty('--smudge-hover-rotation', '-2deg');
      return;
    }

    card.dataset.smudgeCharacter = 'smudge';

    const previous = Number.parseInt(card.dataset.smudgeIndex ?? '-1', 10);
    let index = randomInt(SMUDGES.length);
    if (SMUDGES.length > 1 && index === previous) {
      index = (index + 1 + randomInt(SMUDGES.length - 1)) % SMUDGES.length;
    }

    card.dataset.smudgeIndex = String(index);
    card.style.setProperty(
      '--smudge-hover-image',
      `url("${CDN}/smudges/${SMUDGES[index]}")`
    );
    setPlacement(card);
  };

  const cardFromEvent = (event) => {
    const target = event.target;
    return target instanceof Element ? target.closest('.card') : null;
  };

  const enteredNewCard = (card, relatedTarget) => {
    return !(relatedTarget instanceof Node && card.contains(relatedTarget));
  };

  injectCompatibilityStyles();

  document.addEventListener('pointerover', (event) => {
    const card = cardFromEvent(event);
    if (card && enteredNewCard(card, event.relatedTarget)) assignCharacter(card);
  }, true);

  document.addEventListener('focusin', (event) => {
    const card = cardFromEvent(event);
    if (card && enteredNewCard(card, event.relatedTarget)) assignCharacter(card);
  }, true);

  document.addEventListener('pointerdown', (event) => {
    const card = cardFromEvent(event);
    if (card && event.pointerType === 'touch') assignCharacter(card);
  }, true);
})();
