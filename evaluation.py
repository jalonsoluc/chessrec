import pandas as pd
import chess
import chess.pgn
import chess.engine

normal_position_stats = pd.read_csv('data/metrics/normal_position_stats.csv')
masters_position_stats = pd.read_csv('data/metrics/masters_position_stats.csv')
openings_fen = pd.read_csv('data/metrics/openings_fen7.csv')
openings_evaluations = pd.read_csv('data/metrics/openings_eval.csv')

dataset_map = {
    'normal': normal_position_stats,
    'masters': masters_position_stats
}

def get_win_percentage_score(fen, colour, dataset='normal'):
    position_stats = dataset_map[dataset]
    
    try:
        if colour == 'white':
            win_percentage = position_stats[position_stats['Position'] == fen]['white_win_percentage'].values[0]
        else:
            win_percentage = position_stats[position_stats['Position'] == fen]['black_win_percentage'].values[0]
    except IndexError:
        try:
            win_percentage = openings_fen[openings_fen['fen'] == fen]['winning_percentage'].values[0]
        except IndexError:
            win_percentage = 50
        
    score = (win_percentage / 100)
    return round(score, 2)

def map_engine_path_to_string(engine_path):
    if 'stockfish' in engine_path:
        return 'Stockfish Eval'
    elif 'komodo' in engine_path:
        return 'Komodo Eval'
    elif 'dragon' in engine_path:
        return 'Dragon Eval'
    else:
        return 'other'

def get_position_evaluation_score(boards, engine_path, colour='white', elo=1500, match_type='normal'):
    try:
        score = 0
        for board in boards:
            fen = board.fen()
            score += float(openings_evaluations[openings_evaluations['FEN'] == fen][map_engine_path_to_string(engine_path)].values[0])

    except IndexError:
        # Si el FEN no está en el dataset de evaluaciones de aperturas, se evalúa con el engine
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        score = 0
        for board in boards:
            result = engine.analyse(board, chess.engine.Limit(time=0.1))
            score += (result['score'].relative.score() / 100)
        engine.quit()

    score /= len(boards)
    elo_bonus = 3 - (elo / 3000) * 2
    
    adjusted_score = score if colour == 'white' else -score
    position_value = (adjusted_score + elo_bonus) / (2 * elo_bonus)
    
    return max(min(round(position_value + 0.2, 2), 1), 0)

# Testeo
if __name__ == '__main__':
    boards = []
    board = chess.Board('rnbqkb1r/ppp1pppp/3p4/3nP3/2BP4/8/PPP2PPP/RNBQK1NR b KQkq - 1 4')
    boards.append(board)
    # print(board)

    fen = board.fen()
    print(get_win_percentage_score(fen, 'black', 'normal'))
    print(get_win_percentage_score(fen, 'black', 'masters'))
    print(get_position_evaluation_score(boards, '/usr/local/bin/stockfish', 'black', 2000))
    print(get_position_evaluation_score(boards, 'komodo-14_224afb/OSX/komodo-14.1-64-osx', 'black', 2000))
    print(get_position_evaluation_score(boards, 'dragon_05e2a7/OSX/dragon-avx2-osx', 'black', 2000))