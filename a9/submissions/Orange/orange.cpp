#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <list>
#include <vector>
using namespace std;

int get_factor(list<int> &, vector<int>, int, int);

int main(int argc, char ** argv) {
	/* PARAMETERS */
	if (argc != 6) {
		cerr << "Incorrect arguments! (Expected: <my_id> <num_players> <num_types> <num_to_win> <mode>" << endl;
		return 1;
	}
	int my_id = atoi(argv[1]);
	int num_players = atoi(argv[2]);
	int num_types = atoi(argv[3]);
	int num_to_win = atoi(argv[4]);
	int mode = atoi(argv[5]);

	/* VARIABLES */
	list<int> artifacts;
	vector<int> money_owned(num_players);
	vector<vector<int> > artifacts_owned(num_players);
	int my_bid = 0;

	/* INPUT */
	{
		// Check if the program is initialized (mode == 1) or not (mode == 0)
		if (mode == 0) {
			ifstream input("orange_input.txt");
			if (!input.good()) {
				cerr << "Error! Could not open file \"orange_input.txt\"." << endl;
				return 1;
			}
			int a;
			while (input >> a) artifacts.push_back(a);
			input.close();

			for (vector<vector<int> >::iterator it = artifacts_owned.begin(); it != artifacts_owned.end(); it++) {
				it->resize(num_types);
			}

			for (int i = 0; i < num_players; i++) {
				money_owned.at(i) = 100;
			}
		} else {
			ifstream istate("orange_state.txt");
			stringstream ss;
			string buffer;

			// Line 1: Player Money
			getline(istate, buffer);
			ss.str(buffer);
			for (int i = 0; i < num_players; i++) {
				int m;
				ss >> m;
				money_owned.at(i) = m;
			}
			ss.clear();
			
			// Line 2: Artifacts
			getline(istate, buffer);
			ss.str(buffer);
			int a;
			while (ss >> a) artifacts.push_back(a);
			ss.clear();

			// Lines 3...n: Artifacts Owned
			for (int i = 0; i < num_players; i++) {
				getline(istate, buffer);
				ss.str(buffer);
				while (ss >> a) artifacts_owned.at(i).push_back(a);
				ss.clear();
			}

			istate.close();

			// Get result of last round
			ifstream input("orange_input.txt");

			int winner_id;
			int winner_bid;
			int my_money;
			input >> winner_id >> winner_bid >> my_money;

			// Update money and ownership
			money_owned.at(winner_id) -= winner_bid;
			++artifacts_owned.at(winner_id).at(artifacts.front());
			artifacts.pop_front();

			input.close();
		}
	}

	/* CALCULATION */

	int next_artifact = artifacts.front();
	int num_next_owned = artifacts_owned.at(my_id).at(next_artifact);
	bool still_possible_to_win = false;

	// Check if victory condition is met
	// Also check who has the next artifact up for auction
	for (int i = 0; i < num_players; i++) {
		for (int j = 0; j < num_types; j++) {
			//cout << "player " << i << " has " << artifacts_owned.at(i).at(j) << " of type " << j << endl;
			//cout << "num to win: " << num_to_win << endl;

			if (artifacts_owned.at(i).at(j) >= num_to_win) {
				// Someone won - was it me?
				if (i == my_id) cout << "\nHuh? Did I win?" << endl;
				else cout << "\nPlayer " << i << " wins... GG." << endl;
				return 0;
			}
		}
	}

	/* CALCULATE BID */
	cout << "\nBIDDING FOR: " << next_artifact << " (" << num_next_owned << " already owned..)\n";
	cout << "FUNDS: " << money_owned.at(my_id) << '\n';

	// Normal bet
	int factor = get_factor(artifacts, artifacts_owned.at(my_id), num_players, num_to_win);
	cout << "Factor: " << factor << '\n';
	if (factor > 0) my_bid = min(money_owned.at(my_id), money_owned.at(my_id) / (factor * (num_to_win - num_next_owned)));
	cout << "Bid: " << my_bid << '\n';

	// If the next player needs this to win, bet n+1 (where n is the opponent's remaining money)
	for (int i = 0; i < num_players; i++) {
		if (i == my_id) continue;
		if (artifacts_owned.at(i).at(next_artifact) >= num_to_win - 1) {
			
			my_bid = min(max(my_bid, money_owned.at(i)), money_owned.at(my_id));
		
			cout << "DANGER!!!! Player " << i << " is about to win..\n";

			if (money_owned.at(i) <= money_owned.at(my_id)) {
				cout << "Revised bid: " << my_bid << "\n\n== STALLING ==\n";
				// stall tactics
				time_t starttime = time(NULL);
				while (difftime(time(NULL), starttime) < 2); // wait 2 seconds for opponents' "charity"
			}
		}
	}
	cout << endl;

	/* SAVE STATE */
	{
		ofstream ostate("orange_state.txt");

		// Line 1: Player Money
		for (int i = 0; i < num_players; i++) {
			ostate << money_owned.at(i) << ' ';
		}
		ostate << '\n';

		// Line 2: Remaining Artifacts
		for (list<int>::iterator it = artifacts.begin(); it != artifacts.end(); it++) {
			ostate << *it << ' ';
		}
		ostate << '\n';

		// Line 3-n: Player-Owned Artifacts
		for (int i = 0; i < num_players; i++) {
			//cout << "printing length : " << artifacts_owned.at(i).size() << endl;
			for (vector<int>::iterator it = artifacts_owned.at(i).begin(); it != artifacts_owned.at(i).end(); it++) {
				ostate << *it << ' ';
			}
			ostate << '\n';
		}

		ostate.close();
	}

	/* RESPONSE */
	{
		ofstream output("orange_output.txt");
		output << my_bid;
		output.close();
	}

	//system("pause");
	return 0;
}

int get_factor(list<int> &artifacts, vector<int> my_artifacts, int num_players, int num_to_win) {
	//cout << "generating factor\n";
	if (artifacts.empty()) return 0;

	cout << "Searching top " << num_players << " sets: [ ";

	int target = artifacts.front();
	int factor = 0;
	for (list<int>::iterator it = artifacts.begin(); it != artifacts.end(); it++) {
		if (++my_artifacts.at(*it) >= num_to_win) {
			cout << *it << ' ';
			++factor;
			if (*it == target) {
				cout << "] done\n";
				return factor;
			}
			if (factor >= num_players) break;
		}
	}
	cout << "] done\n";
	return 0;
}
