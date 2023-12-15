# fake_tetris

Puzzle pieces are shaped to resemble seven alphabet letters: ‘L’, ‘l’, ‘T’, ‘t’, ‘z’, ‘c’, and ‘f’. Each piece can create as many as eight distinct shapes, represented as 2D lists/tables, based on its various rotations. You will use binary tables where 1 represents a spot covered by the letter and 0 indicates a spot not covered by the letter.

When prompted, the player can either add a piece to a specific position or remove a piece from the board. 

The add command must follow this format: ‘a <name> <row> <col>’. For example, the command ‘a L 3 1’ means “add the piece ‘L’ at position (3, 1) on the board”. The position of a piece is defined as the location on the board where its top-leftmost corner in its table is placed, i.e., the board location covered by table[0][0]. You may notice that a single 'add' command can result in multiple valid tables for the same piece. In such cases, the player may not fully express their intended shape with the 'add' command alone. The programs presents all possible tables that fit the given position one by one to the player, allowing them to choose the intended one.

The remove command must be of the format ‘r <name>’.

The game continues until the player enters ‘quit’ or the board is filled with all 7 pieces.
