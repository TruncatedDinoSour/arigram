# Bugs
A place of important bugs to fix outside of issues

## States
- 0 -- unsolved
- 1 -- solved (dev build)
- 2 -- solved (release)
- 3 -- won't solve
- 4 -- intended
- 5 -- critical

|   `state`   | `issue`                                                                         | `extra_info`                                                                                                      |     `id`     |
| :---------: | :-----------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------: | :----------: |
|      0      | When pinning chats the UI does not update until arigram is quit                 |                                                                                                                   | 0x0000000000 |
|      1      | API changed, needs refactoring                                                  |                                                                                                                   | 0x0000000001 |
|      0      | Due to API changes and telegram needing more money -- needs sponsor support     |                                                                                                                   | 0x0000000002 |
|      0      | When replying to a message if the message moves you reply to the wrong message  | If you reply to a message in an active conversation the property `self.model.current_msg_id` changes              | 0x0000000003 |

