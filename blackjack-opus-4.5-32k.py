<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎰 Blackjack 21 - Casino Royale</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a472a 0%, #0d2818 50%, #1a472a 100%);
            overflow-x: hidden;
        }

        /* Casino table pattern */
        .table-pattern {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.3) 100%),
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 50px,
                    rgba(255,255,255,0.02) 50px,
                    rgba(255,255,255,0.02) 100px
                );
            pointer-events: none;
            z-index: 0;
        }

        .game-container {
            position: relative;
            z-index: 1;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .title {
            font-size: 3em;
            color: #ffd700;
            text-shadow: 
                0 0 10px #ffd700,
                0 0 20px #ffd700,
                0 0 30px #ff8c00,
                2px 2px 4px rgba(0,0,0,0.5);
            letter-spacing: 3px;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { filter: brightness(1); }
            to { filter: brightness(1.2); }
        }

        .subtitle {
            color: #90EE90;
            font-size: 1.2em;
            margin-top: 5px;
            font-style: italic;
        }

        /* Stats Bar */
        .stats-bar {
            display: flex;
            justify-content: space-around;
            background: linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.4) 100%);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
            border: 2px solid #ffd700;
            box-shadow: 0 0 20px rgba(255,215,0,0.3);
        }

        .stat {
            text-align: center;
        }

        .stat-label {
            color: #aaa;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            color: #ffd700;
            font-size: 1.8em;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255,215,0,0.5);
        }

        .stat-value.chips {
            color: #00ff00;
        }

        /* Game Area */
        .game-area {
            background: radial-gradient(ellipse at center, #2d5a3d 0%, #1a472a 100%);
            border-radius: 200px 200px 20px 20px;
            padding: 30px;
            border: 8px solid #8B4513;
            box-shadow: 
                inset 0 0 50px rgba(0,0,0,0.5),
                0 10px 30px rgba(0,0,0,0.5),
                0 0 0 4px #654321;
            position: relative;
            min-height: 500px;
        }

        .game-area::before {
            content: '♠ ♥ ♣ ♦';
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.5em;
            color: rgba(255,255,255,0.1);
            letter-spacing: 20px;
        }

        /* Hand areas */
        .hand-area {
            margin: 20px 0;
            min-height: 140px;
        }

        .hand-label {
            color: #fff;
            font-size: 1.2em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .hand-score {
            background: rgba(0,0,0,0.6);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #ffd700;
            border: 1px solid #ffd700;
        }

        .hand-score.blackjack {
            background: linear-gradient(135deg, #ffd700, #ff8c00);
            color: #000;
            animation: pulse 0.5s ease-in-out infinite alternate;
        }

        .hand-score.bust {
            background: #dc3545;
            border-color: #dc3545;
            color: #fff;
        }

        @keyframes pulse {
            from { transform: scale(1); }
            to { transform: scale(1.1); }
        }

        .cards {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            min-height: 100px;
            align-items: center;
        }

        /* Cards */
        .card {
            width: 80px;
            height: 120px;
            background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 8px;
            font-size: 1.4em;
            font-weight: bold;
            box-shadow: 
                0 4px 8px rgba(0,0,0,0.3),
                0 0 0 1px rgba(0,0,0,0.1);
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s;
            cursor: default;
            animation: dealCard 0.5s ease-out;
        }

        @keyframes dealCard {
            from {
                transform: translateX(-200px) rotate(-180deg);
                opacity: 0;
            }
            to {
                transform: translateX(0) rotate(0);
                opacity: 1;
            }
        }

        .card.red {
            color: #dc3545;
        }

        .card.black {
            color: #000;
        }

        .card-corner {
            display: flex;
            flex-direction: column;
            align-items: center;
            line-height: 1;
        }

        .card-corner.bottom {
            align-self: flex-end;
            transform: rotate(180deg);
        }

        .card-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2em;
        }

        .card.hidden {
            background: linear-gradient(135deg, #1a237e 0%, #0d1b4c 100%);
            background-image: 
                linear-gradient(135deg, #1a237e 0%, #0d1b4c 100%),
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 10px,
                    rgba(255,255,255,0.05) 10px,
                    rgba(255,255,255,0.05) 20px
                );
        }

        .card.hidden::after {
            content: '🎰';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2.5em;
        }

        /* Message Display */
        .message-area {
            text-align: center;
            margin: 20px 0;
            min-height: 60px;
        }

        .message {
            font-size: 2em;
            font-weight: bold;
            padding: 10px 30px;
            border-radius: 10px;
            display: inline-block;
            animation: messageAppear 0.5s ease-out;
        }

        @keyframes messageAppear {
            from {
                transform: scale(0);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }

        .message.win {
            background: linear-gradient(135deg, #ffd700, #ff8c00);
            color: #000;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
            box-shadow: 0 0 30px rgba(255,215,0,0.5);
        }

        .message.lose {
            background: linear-gradient(135deg, #dc3545, #a71d2a);
            color: #fff;
        }

        .message.push {
            background: linear-gradient(135deg, #6c757d, #495057);
            color: #fff;
        }

        .message.blackjack {
            background: linear-gradient(135deg, #ffd700, #ff6b6b, #ffd700);
            background-size: 200% 200%;
            animation: rainbow 1s ease infinite;
            color: #000;
            font-size: 2.5em;
        }

        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Betting Area */
        .betting-area {
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 2px solid rgba(255,215,0,0.3);
        }

        .bet-label {
            color: #ffd700;
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 15px;
        }

        .bet-chips {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .chip {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            border: 4px dashed rgba(255,255,255,0.5);
            font-size: 1em;
            color: #fff;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            box-shadow: 
                0 4px 8px rgba(0,0,0,0.3),
                inset 0 2px 4px rgba(255,255,255,0.2);
        }

        .chip:hover {
            transform: translateY(-5px) scale(1.1);
            box-shadow: 
                0 8px 16px rgba(0,0,0,0.4),
                0 0 20px currentColor;
        }

        .chip:active {
            transform: translateY(-2px) scale(1.05);
        }

        .chip.chip-5 { background: linear-gradient(135deg, #dc3545, #a71d2a); }
        .chip.chip-10 { background: linear-gradient(135deg, #007bff, #0056b3); }
        .chip.chip-25 { background: linear-gradient(135deg, #28a745, #1e7e34); }
        .chip.chip-50 { background: linear-gradient(135deg, #ff8c00, #cc7000); }
        .chip.chip-100 { background: linear-gradient(135deg, #000, #333); }

        .current-bet {
            text-align: center;
            margin-top: 15px;
            font-size: 1.5em;
            color: #ffd700;
        }

        .current-bet span {
            font-size: 1.5em;
            font-weight: bold;
        }

        /* Controls */
        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .btn {
            padding: 15px 40px;
            font-size: 1.2em;
            font-weight: bold;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255,255,255,0.3),
                transparent
            );
            transition: left 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }

        .btn-hit {
            background: linear-gradient(135deg, #28a745, #1e7e34);
            color: #fff;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
        }

        .btn-hit:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.6);
        }

        .btn-stand {
            background: linear-gradient(135deg, #dc3545, #a71d2a);
            color: #fff;
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
        }

        .btn-stand:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(220, 53, 69, 0.6);
        }

        .btn-double {
            background: linear-gradient(135deg, #ff8c00, #cc7000);
            color: #fff;
            box-shadow: 0 4px 15px rgba(255, 140, 0, 0.4);
        }

        .btn-double:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 140, 0, 0.6);
        }

        .btn-deal {
            background: linear-gradient(135deg, #ffd700, #ff8c00);
            color: #000;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        }

        .btn-deal:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
        }

        .btn-clear {
            background: linear-gradient(135deg, #6c757d, #495057);
            color: #fff;
            padding: 10px 25px;
            font-size: 1em;
        }

        .btn-clear:hover:not(:disabled) {
            transform: translateY(-2px);
        }

        /* Confetti */
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            top: -10px;
            animation: confettiFall 3s linear forwards;
            z-index: 1000;
        }

        @keyframes confettiFall {
            to {
                top: 100vh;
                transform: rotate(720deg);
            }
        }

        /* Modal for game over */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }

        .modal.show {
            display: flex;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background: linear-gradient(135deg, #2d5a3d, #1a472a);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 4px solid #ffd700;
            box-shadow: 0 0 50px rgba(255,215,0,0.3);
            animation: modalPop 0.5s ease;
        }

        @keyframes modalPop {
            from {
                transform: scale(0.5);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }

        .modal-title {
            color: #ffd700;
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        .modal-text {
            color: #fff;
            font-size: 1.3em;
            margin-bottom: 30px;
        }

        /* Responsive */
        @media (max-width: 600px) {
            .title {
                font-size: 2em;
            }

            .card {
                width: 60px;
                height: 90px;
                font-size: 1em;
                padding: 5px;
            }

            .card-center {
                font-size: 1.5em;
            }

            .btn {
                padding: 12px 25px;
                font-size: 1em;
            }

            .chip {
                width: 50px;
                height: 50px;
                font-size: 0.9em;
            }

            .stats-bar {
                flex-wrap: wrap;
                gap: 10px;
            }

            .game-area {
                border-radius: 100px 100px 20px 20px;
                padding: 20px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="table-pattern"></div>
    
    <div class="game-container">
        <header class="header">
            <h1 class="title">♠ BLACKJACK 21 ♠</h1>
            <p class="subtitle">Casino Royale Edition</p>
        </header>

        <div class="stats-bar">
            <div class="stat">
                <div class="stat-label">💰 Chips</div>
                <div class="stat-value chips" id="chips">1000</div>
            </div>
            <div class="stat">
                <div class="stat-label">🏆 Wins</div>
                <div class="stat-value" id="wins">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">📉 Losses</div>
                <div class="stat-value" id="losses">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">🤝 Pushes</div>
                <div class="stat-value" id="pushes">0</div>
            </div>
        </div>

        <div class="game-area">
            <div class="hand-area">
                <div class="hand-label">
                    🎩 Dealer's Hand
                    <span class="hand-score" id="dealer-score">0</span>
                </div>
                <div class="cards" id="dealer-cards"></div>
            </div>

            <div class="message-area">
                <div class="message" id="message" style="display: none;"></div>
            </div>

            <div class="hand-area">
                <div class="hand-label">
                    👤 Your Hand
                    <span class="hand-score" id="player-score">0</span>
                </div>
                <div class="cards" id="player-cards"></div>
            </div>

            <div class="betting-area" id="betting-area">
                <div class="bet-label">💎 Place Your Bet 💎</div>
                <div class="bet-chips">
                    <div class="chip chip-5" onclick="addBet(5)">$5</div>
                    <div class="chip chip-10" onclick="addBet(10)">$10</div>
                    <div class="chip chip-25" onclick="addBet(25)">$25</div>
                    <div class="chip chip-50" onclick="addBet(50)">$50</div>
                    <div class="chip chip-100" onclick="addBet(100)">$100</div>
                </div>
                <div class="current-bet">Current Bet: $<span id="current-bet">0</span></div>
                <div class="controls">
                    <button class="btn btn-clear" onclick="clearBet()">Clear Bet</button>
                    <button class="btn btn-deal" id="btn-deal" onclick="deal()" disabled>Deal Cards</button>
                </div>
            </div>

            <div class="controls" id="game-controls" style="display: none;">
                <button class="btn btn-hit" id="btn-hit" onclick="hit()">Hit</button>
                <button class="btn btn-stand" id="btn-stand" onclick="stand()">Stand</button>
                <button class="btn btn-double" id="btn-double" onclick="doubleDown()">Double</button>
            </div>

            <div class="controls" id="new-game-controls" style="display: none;">
                <button class="btn btn-deal" onclick="newRound()">New Hand</button>
            </div>
        </div>
    </div>

    <div class="modal" id="game-over-modal">
        <div class="modal-content">
            <h2 class="modal-title">💸 Out of Chips! 💸</h2>
            <p class="modal-text">You've run out of chips! Better luck next time!</p>
            <button class="btn btn-deal" onclick="resetGame()">Play Again ($1000)</button>
        </div>
    </div>

    <script>
        // Game State
        let deck = [];
        let playerHand = [];
        let dealerHand = [];
        let chips = 1000;
        let currentBet = 0;
        let wins = 0;
        let losses = 0;
        let pushes = 0;
        let gameInProgress = false;
        let dealerHiddenCard = null;

        // Card suits and values
        const suits = ['♠', '♥', '♣', '♦'];
        const values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];

        // Initialize
        function init() {
            updateDisplay();
        }

        // Create and shuffle deck
        function createDeck() {
            deck = [];
            for (let i = 0; i < 6; i++) { // 6 deck shoe
                for (let suit of suits) {
                    for (let value of values) {
                        deck.push({ suit, value });
                    }
                }
            }
            shuffleDeck();
        }

        function shuffleDeck() {
            for (let i = deck.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [deck[i], deck[j]] = [deck[j], deck[i]];
            }
        }

        // Card value calculation
        function getCardValue(card) {
            if (['J', 'Q', 'K'].includes(card.value)) return 10;
            if (card.value === 'A') return 11;
            return parseInt(card.value);
        }

        function calculateHand(hand) {
            let total = 0;
            let aces = 0;
            
            for (let card of hand) {
                total += getCardValue(card);
                if (card.value === 'A') aces++;
            }
            
            while (total > 21 && aces > 0) {
                total -= 10;
                aces--;
            }
            
            return total;
        }

        // Betting functions
        function addBet(amount) {
            if (gameInProgress) return;
            if (chips >= amount) {
                currentBet += amount;
                chips -= amount;
                updateDisplay();
                document.getElementById('btn-deal').disabled = currentBet === 0;
            }
            playSound('chip');
        }

        function clearBet() {
            if (gameInProgress) return;
            chips += currentBet;
            currentBet = 0;
            updateDisplay();
            document.getElementById('btn-deal').disabled = true;
        }

        // Deal cards
        function deal() {
            if (currentBet === 0) return;
            
            createDeck();
            playerHand = [];
            dealerHand = [];
            gameInProgress = true;
            
            hideMessage();
            
            // Deal cards
            setTimeout(() => {
                playerHand.push(deck.pop());
                renderCards();
                playSound('card');
            }, 100);
            
            setTimeout(() => {
                dealerHand.push(deck.pop());
                dealerHiddenCard = true;
                renderCards();
                playSound('card');
            }, 400);
            
            setTimeout(() => {
                playerHand.push(deck.pop());
                renderCards();
                playSound('card');
            }, 700);
            
            setTimeout(() => {
                dealerHand.push(deck.pop());
                renderCards();
                playSound('card');
                
                // Check for blackjacks
                setTimeout(() => {
                    checkBlackjack();
                }, 300);
            }, 1000);
            
            // Update UI
            document.getElementById('betting-area').style.display = 'none';
            document.getElementById('game-controls').style.display = 'flex';
            document.getElementById('new-game-controls').style.display = 'none';
        }

        function checkBlackjack() {
            const playerTotal = calculateHand(playerHand);
            const dealerTotal = calculateHand(dealerHand);
            
            if (playerTotal === 21 && dealerTotal === 21) {
                dealerHiddenCard = false;
                renderCards();
                endGame('push', '🤝 Both Blackjack - Push!');
            } else if (playerTotal === 21) {
                dealerHiddenCard = false;
                renderCards();
                endGame('blackjack', '🎰 BLACKJACK! 🎰');
            } else if (dealerTotal === 21) {
                dealerHiddenCard = false;
                renderCards();
                endGame('lose', '💀 Dealer Blackjack!');
            }
            
            updateDisplay();
        }

        // Player actions
        function hit() {
            playerHand.push(deck.pop());
            renderCards();
            playSound('card');
            
            const total = calculateHand(playerHand);
            if (total > 21) {
                setTimeout(() => endGame('lose', '💥 BUST! You lose!'), 500);
            } else if (total === 21) {
                stand();
            }
            
            // Disable double after first hit
            document.getElementById('btn-double').disabled = true;
            updateDisplay();
        }

        function stand() {
            document.getElementById('btn-hit').disabled = true;
            document.getElementById('btn-stand').disabled = true;
            document.getElementById('btn-double').disabled = true;
            
            dealerHiddenCard = false;
            renderCards();
            
            dealerPlay();
        }

        function doubleDown() {
            if (chips >= currentBet) {
                chips -= currentBet;
                currentBet *= 2;
                updateDisplay();
                
                playerHand.push(deck.pop());
                renderCards();
                playSound('card');
                
                const total = calculateHand(playerHand);
                if (total > 21) {
                    setTimeout(() => endGame('lose', '💥 BUST! You lose!'), 500);
                } else {
                    setTimeout(() => stand(), 500);
                }
            }
        }

        // Dealer play
        function dealerPlay() {
            function dealerDraw() {
                const dealerTotal = calculateHand(dealerHand);
                
                if (dealerTotal < 17) {
                    setTimeout(() => {
                        dealerHand.push(deck.pop());
                        renderCards();
                        playSound('card');
                        dealerDraw();
                    }, 700);
                } else {
                    setTimeout(() => determineWinner(), 500);
                }
            }
            
            dealerDraw();
        }

        function determineWinner() {
            const playerTotal = calculateHand(playerHand);
            const dealerTotal = calculateHand(dealerHand);
            
            if (dealerTotal > 21) {
                endGame('win', '🎉 Dealer Busts! You Win!');
            } else if (playerTotal > dealerTotal) {
                endGame('win', '🎉 You Win!');
            } else if (dealerTotal > playerTotal) {
                endGame('lose', '😢 Dealer Wins!');
            } else {
                endGame('push', '🤝 Push - Tie Game!');
            }
        }

        function endGame(result, message) {
            gameInProgress = false;
            
            if (result === 'win') {
                chips += currentBet * 2;
                wins++;
                createConfetti();
            } else if (result === 'blackjack') {
                chips += currentBet * 2.5; // Blackjack pays 3:2
                wins++;
                createConfetti();
            } else if (result === 'push') {
                chips += currentBet;
                pushes++;
            } else {
                losses++;
            }
            
            showMessage(message, result);
            currentBet = 0;
            updateDisplay();
            
            document.getElementById('game-controls').style.display = 'none';
            document.getElementById('new-game-controls').style.display = 'flex';
            
            // Check if out of chips
            if (chips <= 0) {
                setTimeout(() => {
                    document.getElementById('game-over-modal').classList.add('show');
                }, 1500);
            }
        }

        function newRound() {
            document.getElementById('betting-area').style.display = 'block';
            document.getElementById('new-game-controls').style.display = 'none';
            document.getElementById('btn-deal').disabled = true;
            document.getElementById('btn-hit').disabled = false;
            document.getElementById('btn-stand').disabled = false;
            document.getElementById('btn-double').disabled = false;
            
            playerHand = [];
            dealerHand = [];
            dealerHiddenCard = null;
            
            renderCards();
            hideMessage();
            updateDisplay();
        }

        function resetGame() {
            document.getElementById('game-over-modal').classList.remove('show');
            chips = 1000;
            wins = 0;
            losses = 0;
            pushes = 0;
            currentBet = 0;
            newRound();
        }

        // Render cards
        function renderCards() {
            const playerCardsEl = document.getElementById('player-cards');
            const dealerCardsEl = document.getElementById('dealer-cards');
            
            playerCardsEl.innerHTML = playerHand.map((card, i) => createCardHTML(card, false, i)).join('');
            dealerCardsEl.innerHTML = dealerHand.map((card, i) => {
                if (i === 1 && dealerHiddenCard) {
                    return `<div class="card hidden" style="animation-delay: ${i * 0.1}s"></div>`;
                }
                return createCardHTML(card, false, i);
            }).join('');
            
            // Update scores
            const playerScore = calculateHand(playerHand);
            const playerScoreEl = document.getElementById('player-score');
            playerScoreEl.textContent = playerScore;
            playerScoreEl.className = 'hand-score';
            if (playerScore === 21 && playerHand.length === 2) {
                playerScoreEl.classList.add('blackjack');
                playerScoreEl.textContent = 'BLACKJACK!';
            } else if (playerScore > 21) {
                playerScoreEl.classList.add('bust');
                playerScoreEl.textContent = playerScore + ' BUST!';
            }
            
            // Dealer score
            const dealerScoreEl = document.getElementById('dealer-score');
            if (dealerHiddenCard) {
                const visibleCard = dealerHand[0];
                dealerScoreEl.textContent = getCardValue(visibleCard) + ' + ?';
            } else {
                const dealerScore = calculateHand(dealerHand);
                dealerScoreEl.textContent = dealerScore;
                dealerScoreEl.className = 'hand-score';
                if (dealerScore === 21 && dealerHand.length === 2) {
                    dealerScoreEl.classList.add('blackjack');
                    dealerScoreEl.textContent = 'BLACKJACK!';
                } else if (dealerScore > 21) {
                    dealerScoreEl.classList.add('bust');
                    dealerScoreEl.textContent = dealerScore + ' BUST!';
                }
            }
        }

        function createCardHTML(card, hidden = false, index = 0) {
            if (hidden) {
                return `<div class="card hidden" style="animation-delay: ${index * 0.1}s"></div>`;
            }
            
            const isRed = card.suit === '♥' || card.suit === '♦';
            const colorClass = isRed ? 'red' : 'black';
            
            return `
                <div class="card ${colorClass}" style="animation-delay: ${index * 0.1}s">
                    <div class="card-corner">
                        <span>${card.value}</span>
                        <span>${card.suit}</span>
                    </div>
                    <div class="card-center">${card.suit}</div>
                    <div class="card-corner bottom">
                        <span>${card.value}</span>
                        <span>${card.suit}</span>
                    </div>
                </div>
            `;
        }

        // Display updates
        function updateDisplay() {
            document.getElementById('chips').textContent = chips;
            document.getElementById('current-bet').textContent = currentBet;
            document.getElementById('wins').textContent = wins;
            document.getElementById('losses').textContent = losses;
            document.getElementById('pushes').textContent = pushes;
        }

        function showMessage(text, type) {
            const messageEl = document.getElementById('message');
            messageEl.textContent = text;
            messageEl.className = 'message ' + type;
            messageEl.style.display = 'inline-block';
        }

        function hideMessage() {
            document.getElementById('message').style.display = 'none';
        }

        // Effects
        function createConfetti() {
            const colors = ['#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ff8c00'];
            
            for (let i = 0; i < 50; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
                    confetti.style.animationDuration = (2 + Math.random() * 2) + 's';
                    document.body.appendChild(confetti);
                    
                    setTimeout(() => confetti.remove(), 4000);
                }, i * 50);
            }
        }

        function playSound(type) {
            // Sound effects would go here
            // Using Web Audio API for simple sounds
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                if (type === 'card') {
                    oscillator.frequency.value = 800;
                    oscillator.type = 'sine';
                    gainNode.gain.value = 0.1;
                } else if (type === 'chip') {
                    oscillator.frequency.value = 1200;
                    oscillator.type = 'sine';
                    gainNode.gain.value = 0.1;
                }
                
                oscillator.start();
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
                oscillator.stop(audioContext.currentTime + 0.1);
            } catch (e) {
                // Audio not supported
            }
        }

        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (!gameInProgress) return;
            
            if (e.key === 'h' || e.key === 'H') hit();
            if (e.key === 's' || e.key === 'S') stand();
            if (e.key === 'd' || e.key === 'D') doubleDown();
        });

        // Initialize game
        init();
    </script>
</body>
</html>