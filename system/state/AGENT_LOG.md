# Agent Log

<!-- Append-only. One line per delegated batch, per review round, and per
     human gate (system/contracts/agent-protocol.md section 6). Format:
     YYYY-MM-DD | phase | pattern | role | rounds | defects | calls | outcome
     pattern: fanout | review | variants | draftahead | firewall | gate | sync
     Gate lines: role = gate name, rounds = operator replies consumed,
     outcome = passed | reworked, defects/calls = "-".
     Derived metric: operator round-trips per gate = sum(gate rounds) /
     count(gate lines). Never rewrite a line; never turn this into prose. -->
