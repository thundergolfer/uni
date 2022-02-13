package algorithms.named;

import java.util.ArrayList;
import java.util.List;

public class NQueens {
    public static void main(String[] args) {
        for (int numQueens=1; numQueens <= 8; numQueens++) {
            List<List<String>> solutions = solve(numQueens);
            for (List<String> solution : solutions) {
                displayQueens(solution);
            }
        }
    }

    private static List<List<String>> solve(int numQueens) {
        int []board = new int[numQueens];
        List<List<String>> solutionsList = new ArrayList<>();
        NQueens.placeQueen(board, 0, numQueens, solutionsList);
        return solutionsList;
    }

    private static void placeQueen(int[] board, int currQueen, int numQueensTotal, List<List<String>> solutionsList) {
        if (currQueen == numQueensTotal) {
            solutionsList.add(solutionToStringBoard(board));
            return;
        }

        for (int row=0; row < numQueensTotal; row++) {
            board[currQueen] = row;
            if (NQueens.allQueensSafe(board, currQueen)) {
                placeQueen(board, currQueen+1, numQueensTotal, solutionsList);
            }
        }
    }

    private static void displayQueens(List<String> board) {
        System.out.print("\n");
        for (String line : board) {
            System.out.println(line);
        }
    }

    private static List<String> solutionToStringBoard(int[] board) {
        int numQueens = board.length;
        List<String> boardAsLines = new ArrayList<>();
        for (int row = 0; row < numQueens; row++) {
            StringBuilder line = new StringBuilder();
            for (int col = 0; col < numQueens; col++) {
                if (board[col] == row) {
                    line.append('Q');
                } else {
                    line.append('.');
                }
            }
            boardAsLines.add(line.toString());
        }
        return boardAsLines;
    }


    private static boolean allQueensSafe(int[] board, int currQueenColumn) {
        for (int column=0; column < currQueenColumn; column++) {
            // Check if any existing queens share a row with the curr queen.
            if (board[column] == board[currQueenColumn]) {
                return false;
            }
            // diagonal check.
            // The key insight is that other queens on the diagonal to the current queen will
            // have the same absolute difference between their column and row numbers.
            // (1, 4) is on the diagonal of (4, 1) and (4, 7)
            // This loop will alway check later columns against earlier columns, but
            // the row of the current queen may be smaller than previously placed queens, so the absolute
            // function is applied to the difference, because either +/- are on the diagonal.
            if ((currQueenColumn - column) == Math.abs(board[currQueenColumn] - board[column])) {
                return false;
            }
        }
        return true;
    }
}
