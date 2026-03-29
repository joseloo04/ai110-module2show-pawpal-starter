# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    -A pet owner needs to track care tasks and get a daily plan. So, there is a person(owner), they have a pet, the pet needs care tasks done, and something needs to organize those task into plan
- What classes did you include, and what responsibilities did you assign to each?
    -Owner: needs to know who they are and how much time they have in a day. They don't really do mch on their own, they just hold that info.
    -Pet: needs to know its name, what kind of animal it is, maybe its age. Same thing, mostly a data holder thate belongs to an Owner.
    -Task: needs to know what it is (a walk, feeding, meds), how long it takes, and how important it is. It belongs to pet.
    -Scheduler: this one actually does something. It takes the Owner's availablle time and the list of Tasks, and figures out what fits and in what order. This is where the logic lives.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
