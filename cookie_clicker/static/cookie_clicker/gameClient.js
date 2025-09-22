// my-second-django-project/cookie_clicker/static/cookie_clicker/gameClient.js

import { GameAPI } from './gameAPI.js';
import { GameUI } from './gameUI.js';

class GameClient {
    constructor() {
        this.api = new GameAPI();
        this.ui = new GameUI(); // GameUI now holds references to all buttons, naa puy logic sa duwa
        this.autoClickerInterval = null;

        this.gameState = {  
            gold: 0, gpc: 1, cps: 0,
            upgrade_gpc_price: 10,
            buy_cps_price: 100, buy_cps_amount: 1,
        };

        this.init();
    }

    init() {
        const bodyDataset = document.body.dataset;
        this.gameState.gold = parseInt(bodyDataset.initialGold);
        this.gameState.gpc = parseInt(bodyDataset.initialGpc);
        this.gameState.cps = parseInt(bodyDataset.initialCps);
        this.gameState.upgrade_gpc_price = parseInt(bodyDataset.initialUpgradeGpcPrice);
        this.gameState.buy_cps_price = parseInt(bodyDataset.initialBuyCpsPrice);
        this.gameState.buy_cps_amount = parseInt(bodyDataset.initialBuyCpsAmount);

        this.ui.update(this.gameState);
        this.ui.attachEventListeners({
            
            onCookieClick: this.handleCookieClick.bind(this),
            onUpgradeGpcClick: this.handleUpgradeGpcClick.bind(this),
            onBuyAutoclickerClick: this.handleBuyAutoclickerClick.bind(this),
            onResetGameClick: this.handleResetGameClick.bind(this),
        });

        this.startAutoClicker();
    }

    // --- Event Handlers ---
    async handleCookieClick() {
        // Access the URL from the button element stored in this.ui
        const data = await this.api.sendAction(this.ui.cookieButton.dataset.url);
        if (data) {
            this.gameState = data;
            this.ui.update(this.gameState);
        }
    }

    async handleUpgradeGpcClick() {
        

        const data = await this.api.sendAction(this.ui.upgradeGpcButton.dataset.url);
        if (data) {
            this.gameState = data;
            this.ui.update(this.gameState);
        }
    }

    async handleBuyAutoclickerClick() {
        

        const data = await this.api.sendAction(this.ui.buyAutoclickerButton.dataset.url);
        if (data) {
            this.gameState = data;
            this.ui.update(this.gameState);
            this.startAutoClicker();
        }
    }

    async handleResetGameClick() {
        // Access the URL from the button element stored in this.ui
        const data = await this.api.sendAction(this.ui.resetGameButton.dataset.url);
        if (data) {
            this.gameState = data;
            this.ui.update(this.gameState);
            this.stopAutoClicker();
            this.startAutoClicker();
        }
    }

    // --- Auto-Clicker Logic, mka mingaw himoon ---
    async autoGenerateGold() {
        if (this.gameState.cps > 0) {
            const data = await this.api.sendAction(document.body.dataset.autoGenerateUrl);
            if (data) {
                this.gameState = data;
                this.ui.update(this.gameState);
            }
        }
    }

    startAutoClicker() {
        this.stopAutoClicker();
        if (this.gameState.cps > 0) {
            this.autoClickerInterval = setInterval(() => this.autoGenerateGold(), 1000);
            console.log(`Auto-clicker started with ${this.gameState.cps} CPS.`);
        } else {
            console.log("No CPS, auto-clicker not started.");
        }
    }

    stopAutoClicker() {
        if (this.autoClickerInterval) {
            clearInterval(this.autoClickerInterval);
            this.autoClickerInterval = null;
            console.log("Auto-clicker stopped.");
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new GameClient();
});