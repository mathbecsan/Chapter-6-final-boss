import Phaser from 'phaser';
import { W, H } from './constants.js';
import PreloadScene from './scenes/PreloadScene.js';
import BossScene from './scenes/BossScene.js';

window.__conductorSettings = { shake: true, flash: false, sound: true };

const game = new Phaser.Game({
  type: Phaser.AUTO,
  width: W,
  height: H,
  parent: 'game',
  backgroundColor: '#050008',
  scene: [PreloadScene, BossScene],
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
  render: { antialias: true, pixelArt: false },
  audio: { disableWebAudio: false },
});

// ---------- DOM shell wiring ----------
const syncToggles = () => {
  const s = window.__conductorSettings;
  [['shake', s.shake], ['flash', s.flash], ['pause-shake', s.shake], ['pause-flash', s.flash]].forEach(([id, on]) => {
    document.querySelectorAll(`#${id} button`).forEach(b => b.classList.toggle('active', (b.dataset.value === 'on') === on));
  });
};
document.querySelectorAll('.segmented').forEach(group => group.addEventListener('click', event => {
  if (!event.target.matches('button')) return;
  const value = event.target.dataset.value === 'on';
  if (group.id.endsWith('shake')) window.__conductorSettings.shake = value;
  if (group.id.endsWith('flash')) window.__conductorSettings.flash = value;
  syncToggles();
}));
syncToggles();

// ---------- pause ----------
document.querySelector('#pause').addEventListener('click', () => window.__pauseBattle?.());
document.querySelector('#resume').addEventListener('click', () => window.__resumeBattle?.());
document.querySelector('#quit').addEventListener('click', () => {
  document.querySelector('#pause-overlay').classList.add('hidden');
  window.__battleScene?.fullReset();
  document.querySelector('#menu').classList.remove('hidden');
});
// Pause / resume toggle. Handled at the DOM level because some browsers
// swallow Escape before Phaser's keyboard plugin receives it.
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape' && e.key !== 'p' && e.key !== 'P') return;
  const overlay = document.querySelector('#pause-overlay');
  const menuOpen = !document.querySelector('#menu').classList.contains('hidden');
  const resultOpen = !document.querySelector('#result').classList.contains('hidden');
  if (menuOpen || resultOpen) return;
  e.preventDefault();
  if (overlay.classList.contains('hidden')) window.__pauseBattle?.();
  else window.__resumeBattle?.();
});

document.querySelector('#start').addEventListener('click', () => {
  document.querySelector('#menu').classList.add('hidden');
  game.sound.unlock();
  window.__startBattle?.();
});

document.querySelector('#again').addEventListener('click', () => {
  document.querySelector('#result').classList.add('hidden');
  window.__battleScene?.fullReset();
  document.querySelector('#menu').classList.remove('hidden');
});

document.querySelector('#mute').addEventListener('click', event => {
  const s = window.__conductorSettings;
  s.sound = !s.sound;
  game.sound.mute = !s.sound;
  event.currentTarget.textContent = s.sound ? 'SOUND ON' : 'SOUND OFF';
});
