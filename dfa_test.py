from automata.fa.dfa import DFA
import string

def main():
    symbols = set(string.printable)
    dfa = DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols=symbols,
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q0', '1': 'q2'},
            'q2': {'0': 'q2', '1': 'q1'}
        },
        initial_state='q0',
        final_states={'q1'}
    )

if __name__ == '__main__':
    main()