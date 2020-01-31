import sys
import random
import double_or_nothing_util as dnUtil
import bot_player as bp
from PyQt5 import QtWidgets, QtGui, QtCore

directoryPath = "playing-cards-assets-master/png/"
backCard = "back.png"


class dnGameWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.isHumanPlayer = True
        self.botPlayer = bp.BotPlayer()
        self.deck = dnUtil.getDeck()
        self.game = dnUtil.DoubleOrNothingGame(self.deck)
        self.initUI()

    # Initializing Functions
    def initUI(self):
        self.createWindowStyle("background1.jpg")
        self.initButtonsAndLabels()
        self.initBotPlayerInterface()
        self.initSlider()
        self.showMainMenu()
        self.show()

    def createWindowStyle(self, path):
        self.setGeometry(100, 100, 600, 300)
        self.setStyleSheet("QPushButton { font: 10pt Arial }")
        bg_img = QtGui.QImage(path).scaled(QtCore.QSize(
            600, 300))  # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(bg_img))  # 10 = WindowRole
        self.setPalette(palette)
        self.centerWindow()

    def centerWindow(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def initButtonsAndLabels(self):
        self.initMainMenu()
        self.initTextBox()
        self.initGameButtons()

        self.card1 = QtWidgets.QLabel(self)
        self.card2 = QtWidgets.QLabel(self)

        color = QtGui.QColor(229, 229, 229)
        self.setLabelBgColor(self.card1, color, 255)
        self.setLabelBgColor(self.card2, color, 255)

    def createButton(self, name, size, pos, func):
        btn = QtWidgets.QPushButton(name, self)
        btn.resize(size[0], size[1])
        btn.move(pos[0], pos[1])
        btn.clicked.connect(func)
        return btn

    def initMainMenu(self):
        self.computerBtn = self.createButton(name="Computer",
                                             size=(100, 100), pos=(150, 100), func=self.startBotGame)
        self.playBtn = self.createButton(name="Play",
                                         size=(100, 100), pos=(350, 100), func=self.startHumanGame)
        menuBtn = self.createButton(name="Main Menu",
                                    size=(75, 20), pos=(525, 0), func=self.showMainMenu)
        exitBtn = self.createButton(name="Exit Game",
                                    size=(75, 30), pos=(525, 270), func=self.exitApp)

    def initTextBox(self):
        self.textbox = QtWidgets.QLabel("", self)
        self.textbox.resize(200, 30)
        self.textbox.move(375, 30)
        self.textbox.setStyleSheet("QLabel { font: 9pt Lucida Console; \
										background-color: black; \
										color: #88d471 }")
        self.textbox.setAlignment(QtCore.Qt.AlignHCenter)
        self.textbox.setFrameStyle(
            QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

    def initGameButtons(self):
        self.higherBtn = self.createButton(name="Higher",
                                           size=(75, 75), pos=(390, 100), func=self.gameChoose)
        self.lowerBtn = self.createButton(name="Lower",
                                          size=(75, 75), pos=(490, 100), func=self.gameChoose)
        self.contBtn = self.createButton(name="Continue?",
                                         size=(75, 20), pos=(390, 120), func=self.gameStep)
        self.restartBtn = self.createButton(name="Restart",
                                            size=(75, 20), pos=(440, 120), func=self.gameRestart)
        self.gameExitBtn = self.createButton(name="Exit",
                                             size=(75, 20), pos=(440, 150), func=self.gameExit)

    def setLabelBgColor(self, label, color, alpha):
        label.setAutoFillBackground(True)
        values = "{r}, {g}, {b}, {a}".format(r=color.red(),
                                             g=color.green(),
                                             b=color.blue(),
                                             a=alpha)
        label.setStyleSheet(
            "QLabel { background-color: rgba(" + values + "); }")
        label.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        label.setLineWidth(2)

    def initSlider(self):

        self.sliderLabel = QtWidgets.QLabel('Risk Level', self)
        self.sliderLabel.move(375, 155)
        self.sliderLabelHigh = QtWidgets.QLabel('High', self)
        self.sliderLabelHigh.move(375, 200)
        self.sliderLabelLow = QtWidgets.QLabel('Low', self)
        self.sliderLabelLow.move(550, 200)

        color = QtGui.QColor(255, 255, 255)
        self.setLabelBgColor(self.sliderLabel, color, 255)
        self.setLabelBgColor(self.sliderLabelHigh, color, 255)
        self.setLabelBgColor(self.sliderLabelLow, color, 255)

        self.slider = QtWidgets.QSlider(self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.move(375, 175)
        self.slider.resize(200, 30)
        self.slider.setTickPosition(3)
        self.slider.setValue(50)

        self.slider.valueChanged.connect(self.changeSliderValue)

    def changeSliderValue(self):
        self.game.setRisk(self.slider.value())

    # Menu Functions
    def showMainMenu(self):
        """
        Show menu buttons and hide all non-menu buttons.
        """
        self.game.resetGame()
        self.playBtn.show()
        self.computerBtn.show()

        self.textbox.hide()
        self.higherBtn.hide()
        self.lowerBtn.hide()
        self.contBtn.hide()
        self.restartBtn.hide()
        self.gameExitBtn.hide()
        self.card1.hide()
        self.card2.hide()
        self.valsBox.hide()
        self.initEntry.hide()
        self.nextEntry.hide()
        self.slider.hide()
        self.sliderLabel.hide()
        self.sliderLabelHigh.hide()
        self.sliderLabelLow.hide()

    def startHumanGame(self):
        """
        Transition buttons to human game.
        """
        self.isHumanPlayer = True
        self.playBtn.hide()
        self.computerBtn.hide()
        self.textbox.show()
        self.gameStep()
        self.card1.show()
        self.card2.show()

    def startBotGame(self):
        """
        Transition buttons to bot-assisted game.
        """
        self.isHumanPlayer = False
        self.sliderLabel.show()
        self.sliderLabelHigh.show()
        self.sliderLabelLow.show()
        self.playBtn.hide()
        self.computerBtn.hide()
        self.textbox.show()
        self.valsBox.show()
        self.initEntry.show()
        self.slider.show()
        self.setGlobalMsg("Enter the first card value.")

    def exitApp(self):
        """
        Exit program. Used for exit button.
        """
        sys.exit()

    def setGlobalMsg(self, string):
        """
        Set the text for the textbox.
        """
        self.textbox.setText(string)

    # Game step functions

    def gameStep(self):
        """ 
        Go to the next step of the game. 
        If game started, draw a card from the deck and set it has the left card. 
        Otherwise, move the right card to the left.
        """
        g = self.game
        deck = g.getGameDeck()

        if g.getRandCard2() is None:
            newCard = dnUtil.drawCard(deck)
            g.setRandCard(newCard)
            self.botPlayer.updateBotCounts(newCard)
        else:
            g.setRandCard(g.getRandCard2())
            g.setRandCard2(None)

        randCard = g.getRandCard()
        randCard2 = g.getRandCard2()

        self.updateCardImage(self.card1, randCard, [20, 20])
        self.updateCardImage(self.card2, backCard, [200, 20])

        if self.isHumanPlayer:
            self.gameStepHuman()
        else:
            self.gameStepBot(randCard, randCard2)

    def gameStepHuman(self):
        """
        Human player only needs to update score.
        """
        g = self.game
        score = g.getScore()
        self.setGlobalMsg("Score: " + str(score) +
                          ", High Score: " + str(g.getHighScore()))
        self.playerPhase()

    def gameStepBot(self, randCard, randCard2):
        """
        Bot player needs to update its variables.
        Also, get the best action for current step.
        """
        g = self.game
        bp = self.botPlayer
        self.contBtn.hide()
        bp.setBase(randCard)
        bp.setUnknown(randCard2)
        state = bp.getState()
        bestAction = bp.getAction(g, state)
        score = g.getScore()
        self.setGlobalMsg("Score: " + str(score) +
                          ", High Score: " + str(g.getHighScore()) +
                          "\n Best action is " + bestAction)

    def updateCardImage(self, label, path, pos):
        """	
        Get the card image from file path, then set picture to the LABEL at POS	
        """
        label.move(pos[0], pos[1])
        pixmap = QtGui.QPixmap(directoryPath + path).scaledToWidth(150)
        label.setPixmap(pixmap)

    def playerPhase(self):
        """
        Player phase is when player predicts if the next card is higher or lower.
        """
        self.higherBtn.show()
        self.lowerBtn.show()
        self.contBtn.hide()
        self.restartBtn.hide()
        self.gameExitBtn.hide()

    def transitionPhase(self, lose=True):
        """
        Player must decide to continue (if possible) or exit.
        """
        self.higherBtn.hide()
        self.lowerBtn.hide()
        if not lose:
            self.contBtn.show()
        self.gameExitBtn.show()

    def gameChoose(self):
        """ 
        Play the game. User clicks on a choice button. 
        We get a draw a card from the deck.
        Compare choice with drawn card and send to next state. 
        """
        g = self.game
        deck = g.getGameDeck()
        randCard = g.getRandCard()
        randCard2 = dnUtil.drawCard(deck)

        g.setRandCard2(randCard2)
        self.updateCardImage(self.card2, randCard2, [200, 20])
        if not self.isHumanPlayer:
            self.botPlayer.setUnknown(randCard2)
            self.botPlayer.updateBotCounts(randCard2)
        choice = win.sender().text()
        self.gameEval(randCard, randCard2, choice)

    def gameEval(self, randCard, randCard2, choice):
        """
        Check if the player chose the correct action.
        """
        decision = dnUtil.gameDecision(randCard, randCard2, choice)
        if decision == 0:
            self.gameTie()
        elif decision == 1:
            self.gameWin()
        elif decision == -1:
            self.gameLose()

    def gameWin(self):
        """ 
        If you win, update score, ask if exit or continue. 
        """
        g = self.game
        score = g.incrementScore()
        self.setGlobalMsg("Score: " + str(score) +
                          ", High Score: " + str(g.getHighScore()))
        self.gameExitBtn.move(490, 120)
        self.transitionPhase(False)
        if not self.isHumanPlayer:
            self.botDecideExitPhase()

    def gameTie(self):
        """	
        If you tie, ask if exit or continue. 
        """
        self.gameExitBtn.move(490, 120)
        self.transitionPhase(False)
        if not self.isHumanPlayer:
            self.botDecideExitPhase()

    def gameLose(self):
        """ 
        If you lose, show score and exit. 
        """
        if not self.isHumanPlayer:
            self.botPlayer.setScore(0)
            self.botPlayer.setLoseBool(True)
        self.gameExitBtn.move(440, 120)
        self.transitionPhase(True)

    def botDecideExitPhase(self):
        """
        Bot updates information and chooses post-choice strategy.
        """
        g = self.game
        state = self.botPlayer.getState()
        bestAction = self.botPlayer.getAction(g, state)
        score = g.getScore()
        self.setGlobalMsg("Score: " + str(score) +
                          ", High Score: " + str(g.getHighScore()) +
                          "\n Best action is " + bestAction)
        if bestAction == "Continue?":
            self.gameExitBtn.hide()
        else:
            self.contBtn.hide()

    def gameExit(self):
        """	
        End the game, obtain final score. 
        """
        self.restartBtn.move(440, 120)
        self.restartBtn.show()
        self.contBtn.hide()
        self.gameExitBtn.hide()

    def gameRestart(self):
        """ 
        Reset the game and deck. 
        """
        g = self.game
        score = g.resetScore()
        self.setGlobalMsg("Score: " + str(score) +
                          ", High Score: " + str(g.getHighScore()))
        g.resetDeck()
        g.setRandCard2(None)
        if not self.isHumanPlayer:
            self.botPlayer = bp.BotPlayer()
            self.botPlayer.setScore(0)

        self.gameStep()

    # Bot related functions
    def initBotPlayerInterface(self):
        """
        Setup drop-down menus for values and suits.
        """
        self.valsBox = QtWidgets.QComboBox(self)
        self.valsBox.setObjectName(("Values"))
        for value in dnUtil.valuesList:
            self.valsBox.addItem(value.upper())
        self.valsBox.resize(75, 20)
        self.valsBox.move(375, 100)

        self.initEntry = self.createButton(name='Display card',
                                           size=(85, 30), pos=(435, 220), func=self.initBot)
        self.nextEntry = self.createButton(name='Display card',
                                           size=(85, 30), pos=(435, 220), func=self.onClick)

    def initBot(self):
        """
        Get information from input to set first card.
        """
        g = self.game
        bp = self.botPlayer

        self.initEntry.hide()
        entry1 = str(self.valsBox.currentText()).lower()
        randomSuit = dnUtil.suitsList[random.randint(0, 3)]
        card = dnUtil.getCardString(entry1, randomSuit)
        g.setRandCard(card)
        bp.setBase(card)
        bp.setUnknown(None)
        bp.updateBotCounts(card)
        self.updateCardImage(self.card1, card, [20, 20])
        self.updateCardImage(self.card2, backCard, [200, 20])

        state = bp.getState()
        bestAction = bp.getAction(g, state)
        score = g.getScore()
        self.setGlobalMsg("Score: " + str(score) +
                          ", High Score: " + str(g.getHighScore()) +
                          "\n Best action is " + bestAction)
        self.nextEntry.show()
        self.card1.show()
        self.card2.show()

    def onClick(self):
        """ 
        Display the card entered in the input text fields. 
        Give the best action for the current state.
        """
        g = self.game
        bp = self.botPlayer
        entry1 = str(self.valsBox.currentText()).lower()

        randomSuit = dnUtil.suitsList[random.randint(0, 3)]
        card = dnUtil.getCardString(entry1, randomSuit)
        g.setRandCard2(card)
        bp.setUnknown(card)
        bp.updateBotCounts(card)
        self.updateCardImage(self.card2, card, [200, 20])

        base = g.getRandCard()
        baseVal = dnUtil.getValue(base)
        otherVal = dnUtil.getValue(card)
        if dnUtil.compareValue(baseVal, otherVal) > 0:
            self.gameEval(base, card, "Lower")
        else:
            self.gameEval(base, card, "Higher")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = dnGameWindow()
    sys.exit(app.exec_())