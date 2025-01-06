class PrisonersDilemma:
    p1 = None
    p2 = None

    def __init__(self, player1, player2):
        assert player1 != None
        assert player2 != None
        self.p1 = player1
        self.p2 = player2
        self.total_scores1 = [0] * 3 # [-1] total score
        self.total_scores2 = [0] * 3
        self.scores1 = []
        self.scores2 = []
        self.choices1 = []
        self.choices2 = []


    def play(self):
        choice1 = self.p1.choose(self.choices1, self.scores1, self.total_scores1,
                self.choices2, self.scores2, self.total_scores2)
        choice2 = self.p2.choose(self.choices2, self.scores2, self.total_scores2,
                self.choices1, self.scores1, self.total_scores1)

        score1 = score2 = 1
        if choice1 == 1 and choice2 == 1:
            score1 = score2 = 3
        elif choice1 == 1 and choice2 == 0:
            score1 = 0
            score2 = 5
        elif choice1 == 0 and choice2 == 1:
            score1 = 5
            score2 = 0
        else:
            score1 = score2 = 1

        self.choices1.append(choice1)
        self.choices2.append(choice2)

        self.scores1.append(score1)
        self.scores2.append(score2)

        self.total_scores1[choice1] += score1
        self.total_scores1[-1] += score1
        self.total_scores2[choice2] += score2
        self.total_scores2[-1] += score2


    def name(self) -> str:
        p1_name = self.p1.__class__.__name__
        p2_name = self.p2.__class__.__name__
        return f"{p1_name} vs {p2_name}"
