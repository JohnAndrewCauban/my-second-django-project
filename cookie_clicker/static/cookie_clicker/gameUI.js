// my-second-django-project/cookie_clicker/static/cookie_clicker/gameUI.js

export class GameUI {
    constructor() {
        // Get all necessary DOM elements once
        this.goldCountSpan = document.getElementById('gold-count');
        this.gpcCountSpan = document.getElementById('gpc-count');
        this.cpsCountSpan = document.getElementById('cps-count');
        this.upgradeGpcPriceSpan = document.getElementById('upgrade-gpc-price');
        this.buyCpsPriceSpan = document.getElementById('buy-cps-price');

        // Store button elements as properties of the UI class
        this.cookieButton = document.getElementById('cookie-button'); 
        this.upgradeGpcButton = document.getElementById('upgrade-gpc-button');
        this.buyAutoclickerButton = document.getElementById('buy-autoclicker-button');
        this.resetGameButton = document.getElementById('reset-game-button'); 
    }

    update(gameState) {
        // Update text content for all stats
        this.goldCountSpan.textContent = gameState.gold;
        this.gpcCountSpan.textContent = gameState.gpc;
        this.cpsCountSpan.textContent = gameState.cps;
        this.upgradeGpcPriceSpan.textContent = gameState.upgrade_gpc_price;
        this.buyCpsPriceSpan.textContent = gameState.buy_cps_price;

        // Update disabled states for buttons based on current gold
        this.upgradeGpcButton.disabled = gameState.gold < gameState.upgrade_gpc_price;
        this.buyAutoclickerButton.disabled = gameState.gold < gameState.buy_cps_price;
    }

    attachEventListeners(handlers) {
        this.cookieButton.addEventListener('click', handlers.onCookieClick);
        this.upgradeGpcButton.addEventListener('click', handlers.onUpgradeGpcClick);
        this.buyAutoclickerButton.addEventListener('click', handlers.onBuyAutoclickerClick);
        this.resetGameButton.addEventListener('click', handlers.onResetGameClick);
    }
}