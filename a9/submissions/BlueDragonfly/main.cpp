#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<iostream>
#include<vector>
using namespace std;
class Player{
public:
	int budget;
	int itemCnt[20];
	double itemScore[20];
	int total;
	int playerId;
	Player(int playerId){
		this->playerId = playerId;
		budget = 100;
		total =0;
		for(int i=0; i<20; ++i){
			itemCnt[i] = 0;
		}
	}
	void winItem(int itemId, int bid){
		itemCnt[itemId]++;
		this->budget -= bid;
		total++;
	}
};
static vector<Player> players;
static int myId;
class Game{
public:
	int numberOfItemType;
	int numberOfItems;
	int numberOfPlayers;
	int goal;
	int items[11000];
	int currentItem;
	int myPlayerId;
	Game(){
		currentItem = 0;
		//printf("start parsing\n");
		scanf("%d %d %d %d", &myPlayerId, &numberOfPlayers, &numberOfItemType, &goal);
		myId = myPlayerId;
		numberOfItems = 10000;
		
		for(int i=0; i<numberOfItems; ++i){
			scanf("%d", &items[i]);
			//printf("%d: %d ", i, items[i]);
		}
		
		 for(int i=0; i<numberOfPlayers; ++i){
		 Player newplayer(i);
		 players.push_back(newplayer);
		 } 
	}
	int update(){
		int winnerID, winnerBid, budget;
		scanf("%d %d %d", &winnerID, &winnerBid, &budget);
		players[winnerID].winItem(items[currentItem], winnerBid);
		return budget;
	}
	void getScore(int bias){ 
		int i = myPlayerId;
		for(int j=0; j<numberOfItemType; ++j){
			int cnt=0;
			int k;
			for(k=currentItem; players[i].itemCnt[j]+cnt< goal + bias; ++k){
				if(items[k] == j) cnt++;
			}
			players[i].itemScore[j] =1000-k;
			
		}
		
	}
};
int min(int a, int b){
	printf("%d vs %d\n", a,b);
	return a>b? b:a;
}
int findTarget(Game& g){
	int index;
	double best = 0;
	for(int i=0; i<g.numberOfItemType; ++i){
		if(players[myId].itemScore[i] > best){
			best = players[myId].itemScore[i];
			index = i;
		}
	}
	return index;
}
int main(){
	Game g;
	int a = 10000;
	string s;
	int bid;
	int target1, target2;
	int mode = 0;
	while(a--){
		if(players[g.myPlayerId].total==0){
			g.getScore(0);			
			target1 = findTarget(g);
			g.getScore(int(g.goal/3));			
			target2 = findTarget(g);
			if(target1==target2) mode =0;
			else mode =1;
		}
		if(g.items[g.currentItem] ==  target1){
			
			if(players[g.myPlayerId].itemCnt[target1] < int(g.goal/3))
				bid = int(100/g.goal) + mode;
			else if(players[g.myPlayerId].itemCnt[target1] < int(g.goal/2))
				bid = int(100/g.goal);
			else if(players[g.myPlayerId].itemCnt[target1] == g.goal - 1)
				bid = players[g.myPlayerId].budget;
			else
				bid = int(100/g.goal)-mode;
		} 
		else{
			bid = 0;
		}
		bid = min(bid, players[g.myPlayerId].budget);
		printf("-%d\n", bid);
		getline(cin, s);
		players[g.myPlayerId].budget = g.update();
		g.currentItem++;
	}
	return 0;
}
