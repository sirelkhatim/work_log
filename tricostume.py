def GLIE(convergence_iters, iter_num, final_val):
   if iter_num <= convergence_iters:
       epsilon = (((final_val - 1)/convergence_iters)*iter_num) + 1
   else:
       epsilon = final_val
   return epsilon

def epsilon_greedy(Qs, epsilon):
   policy_s = epsilon * np.ones(Qs.shape[0])/Qs.shape[0]
   max_index = np.argmax(Qs)
   policy_s[max_index] = 1 - epsilon + (epsilon/Qs.shape[0])
   return policy_s

def choose_At1_from_Q(env, state, Q, epsilon):
   if state in Q:
           probs = epsilon_greedy(Q[state], epsilon)
           action = np.random.choice(np.arange(env.nA), p=probs)
   else:
       action = env.action_space.sample()
   return action

def sarsa(env, num_episodes, alpha, gamma=1.0):
   # initialize action-value function (empty dictionary of arrays)
   Q = defaultdict(lambda: np.zeros(env.nA))
   # initialize performance monitor
   # loop over episodes
   convergence_iters = int(num_episodes*7/8)
   temp_scores = deque(maxlen=num_episodes)
   avg_scores = deque(maxlen=num_episodes)

   for i_episode in range(1, num_episodes+1):
       # monitor progress
       epsilon = GLIE(convergence_iters, i_episode, 0.1)
       if i_episode % 1 == 0:
           print("\rEpisode {}/{} epsilon = {} .".format(i_episode, num_episodes, epsilon), end="")
           sys.stdout.flush()

       ## TODO: complete the function
       st = env.reset()
       at = choose_At1_from_Q(env, st, Q, epsilon)
       index = 0
       episode_score = 0
       while True:
           #print("\rindex: {} ".format(index), end="")
           #sys.stdout.flush()
           # Take action At, observe (Rt+1, St+1)
           #print("st = " + str(st) + " at = " + str(at))
           st_1, rt_1, done, info = env.step(at)
           episode_score += rt_1

           if done:
               #print(" Episode length: " + str(index))
               temp_scores.append(episode_score)
               break

           #print("st_1 = " + str(st_1) + " rt_1 = " + str(rt_1) + "done: " + str(done))
           # Choose action At+1
           at_1 = choose_At1_from_Q(env, st_1, Q, epsilon)
           # Update action value
           Q[st][at] = Q[st][at] + alpha*((rt_1 + (gamma*Q[st_1][at_1])) - Q[st][at])

           st = st_1
           at = at_1
           index += 1
           if (i_episode % 100 == 0):
               avg_scores.append(np.mean(temp_scores))

   # plot performance
   plt.plot(np.linspace(0,num_episodes,len(avg_scores),endpoint=False), np.asarray(avg_scores))
   plt.xlabel('Episode Number')
   plt.ylabel('Episode Reward')
   plt.show()

   return Q