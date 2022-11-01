class Player{
    Cell puck;
    Cell play(Board board, Dice dice) {
        int score = dice.roll();
        int newScore = (puck == null ? 0 : puck.value ) + score;
        puck = move(board, newScore)
        return puck;
    }

    Cell move(Board board, int score) {
        Cell newCell = board.getCell(score);
        if (newCell.to != null) {
            newCell = newCell.to;
        }
        return newCell;
    }

    boolean isWinner() {
       return puck.type == TYPE.TARGET;
    }
}

class Dice {
    int roll();
}
class Cell {
    Type type;
    Cell to;
    int value;
}

enum Type {
    SNAKE, LADDER, TARGET
}


class Board {
    Map<Integer, Cell> cells;
}
  
class Game {
    Board board;
    List<Player> players;
    Dice dice;  

   start() {
       board = createBoard();
       players = createPlayers();
       dice = new Dice();
       while(!playTerminated()) {
            for(Player p : players) {
                 p.play(board, dice);
                 if (p.isWinner()) {
                     declareWinner();
                     break;
                 }
       }
}
