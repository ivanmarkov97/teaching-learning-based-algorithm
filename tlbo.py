from __future__ import print_function
import numpy as np

def fitness_func(X):
	A = 10
	return A * len(X) + sum([x**2 - A*np.cos(2.0 * np.pi * x) for x in X])

class TLBO():
	def __init__(self, n_learners, dim, tol=1e-5, early_stop=30, f=None):

		self.n_learners = n_learners
		self.Dim = dim
		self.fitness = f
		self.tol = tol
		self.early_stop = early_stop

		self.learners = np.array([np.random.uniform(-20, 20, size=(self.Dim,))])
		for _ in range(self.n_learners - 1):
			self.learners = np.vstack((self.learners, np.random.uniform(-20, 20, size=(self.Dim,))))


	def minimize(self):
		run = True
		iteration = 0
		iteration_teacher_value = []
		min_teacher_value = min([self.fitness(learner) for learner in self.learners])

		while run:
			results = [self.fitness(learner) for learner in self.learners]
			self.teacher = self.learners[np.argmin(results)]
			self.x_mean = sum(self.learners) / len(self.learners)
			iteration_teacher_value.append(min(results))

			for pos, learner_old in enumerate(self.learners):
				Tf = np.round(np.random.uniform(1, 2), 0)
				learner_new = learner_old + np.random.uniform(0, 1, size=(self.Dim,)) * (self.teacher - Tf * self.x_mean)
				if self.fitness(learner_new) < self.fitness(learner_old):
					self.learners[pos] = learner_new

				to_select_learner = list(range(self.learners.shape[0]))
				to_select_learner.remove(pos)
				learner_to_interract = np.random.choice(to_select_learner)

				if self.fitness(self.learners[pos]) <= self.fitness(self.learners[learner_to_interract]):
					learner_interraction = self.learners[pos] + \
									np.random.uniform(0, 1, size=(self.Dim,)) * \
									(self.learners[pos] - self.learners[learner_to_interract])

				elif self.fitness(self.learners[pos]) > self.fitness(self.learners[learner_to_interract]):
					learner_interraction = self.learners[pos] + \
									np.random.uniform(0, 1, size=(self.Dim,)) * \
									(self.learners[learner_to_interract] - self.learners[pos])

				if self.fitness(learner_interraction) < self.fitness(self.learners[pos]):
					self.learners[pos] = learner_interraction
			

			if len(iteration_teacher_value) % self.early_stop == 0 and len(iteration_teacher_value) > 0:
				if min_teacher_value - iteration_teacher_value[-1] < self.tol:
					run = False
				else:
					min_teacher_value = iteration_teacher_value[-1]
					print('func ', self.fitness(self.teacher))
					print('iteration ', iteration + 1)
			iteration += 1

		results = [self.fitness(learner) for learner in self.learners]
		self.teacher = self.learners[np.argmin(results)]
		self.x_mean = sum(self.learners) / len(self.learners)

		print('teacher ',self.teacher)
		print('func ', self.fitness(self.teacher))

if __name__ == '__main__':
	tlbo = TLBO(n_learners=50, dim=32, tol=1e-5, early_stop=30, f=fitness_func)
	tlbo.minimize()
