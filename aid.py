#!/usr/bin/env python3



def standardize_failover(input_string):
    """Standardizes failover variations to 'Failover'."""
    if not input_string:
        return "Error: Input string is empty."

    pattern = r"\b(fail[\s\-/]*o[\s\-/]*v[\s\-/]*e?r|fo|failvover|faiolver|failolver|faover|faillover|feilover|failove|failver|faillover|failoverbackup)\b|failover\b|failover\w+"
    if re.search(pattern, input_string, re.IGNORECASE):
        return "Failover"
    else:
        return "nothing changed"

# ... rest of the script ...

test_values = [
    "Lane 1 Failover", "Set 2", "Set 1 Failover", "Lane One Failover",
    "Failover", "Failover 1", "Failvover", "Lane 2 Failover",
    "Lane 1- Failover", "DT failover", "Lane 1-Failover", "Lane 1 Fail Over",
    "DT Lane 1 Failover", "Drive Thru Failover", "Lan 1 Failover",
    "DT1 Failover", "Lanes 1 Failover", "Failover lane 1",
    "Lane 1 Faiolver", "DT Failover 1", "Lane 1 Failover.",
    "Lane 1 - Failover", "Pilot DT Failover", "Fail Over Lane 1",
    "Lnae 1 Failover", "DT Lane 2", "Lane\xa0 1 failover",
    "DT AIO Failover", "DT L1 FO", "Lan1 Failover", "Lane 1 Failolver",
    "Lane1- Failover", "Lane 1 Faillover", "Lane 1 Filover",
    "Lane 1 Faover", "Drive Through Failover", "DT Lane Failover",
    "Lane 1 FO", "DT - Failover", "ODMB 1 Failover", "ODMB 2 Failover",
    "Lane1 - Failover", "DT 1 Failover", "AIO DT Failover", "ODMB L2",
    "Drive- Thru failover", "Lane 1 -Failover", "DT Lane 2 Failover",
    "DT FO", "ODMB FO", "Lane Failover", "Lane 1\xa0 - Failover",
    "DT Lane 1 FO", "Lane1 Failover", "DT LN 2",
    "Drive- Thru \xe2\x82\xac\xe2\x80\x93 Presell Failover", "Lane 1Failover",
    "DT Lane 1 (Failover)", "Lane 2- Failover", "DT Lane 2 FO",
    "Line 1 Failover", "Presell 1 Failover", "Presell 2",
    "Presell failover", "Presell lane 1 Failover", "Presell 1Failover",
    "Presell1 Failover", "Indoor monitoring", "Failover FC",
    "Non-OT Horizontal Failover", "FC Failover 1", "FC - Failover",
    "FC 1 Failover", "FC 1- Failover", "FC 1 - Failover",
    "Front Counter Failover", "Front Counter 1 Failover", "FC1 Failover",
    "FC 1-Failover", "Dunkin donuts FC Failover", "FC Failover - DD",
    "Front Counter Failover 0", "Front Counter Failaover",
    "Frontcounter Failover", "Front counter fail over", "DD FC Failover 1",
    "Dunkin Front Counter Failover", "FC Fail Over", "FC Feilover",
    "Front Counter Failove", "Front Counter Failver", "FC Faillover",
    "FC 1\xa0 Failover", "Front Counter - Failover",
    "Front Counter Failover\xa0 FC Failover", "Fronter Counter Failover",
    "FC Backup", "Set 2 failover", "DD FC 1 FO", "FC\xa0 Failover",
    "Front Screen Failover", "FC 1\xa0 - Failover", "Frount Counter Failover",
    "Front Counter 1 (Failover)", "Front\xa0 Counter Failover",
    "Set 1 Backup", "DD FC Failover", "FC DD - Failover",
    "FC Failover 2", "DD Front Counter Failover", "Front Counter1 Failover",
    "Front Couter Failover", "FC 1_Failover", "Front Counter DD Failover",
    "Front Counter\xa0 Failover", "Frount Couter Failover",
    "Fronte counter 1 failover", "Leadership Circle Failover",
    "2nd Floor Outside 209 Failover", "3rd Floor Failover",
    "FC Failover", "Front Counter 0 - Failover",
    "Front Counter 0 - Failover.", "Set 0 Failover", "DD FC FO",
    "Front Counter Dunkin Failover", "FC FO", "Dunkin FC failover",
    "Baskin FC Failover", "Baskin Front Counter Failover 0",
    "Baskins FC Failover", "Baskin Front Counter Failover",
    "BR1 Failover", "Front Counter 2 Failover",
    "Front Counter Baskin Failover 0", "Baskin Robbins Failover",
    "BR Front Counter Failover", "FC BR - Failover",
    "Baskin Font Counter Failover", "FC 2 Failover",
    "Baskin Robbins FC Failover 0", "Baskin Robbins FC Failover",
    "FC 0 Failover", "Baskin Robbins Front Counter FA",
    "FC Failover - BR", "FC Baskin failover",
    "Front Counter Baskin Failover", "Br Failover",
    "BB Front Counter Failover", "Front Counter 0 Failover",
    "Front Counter 1 Baskins Failover", "FC2 Failover",
    "FC FAILOVER BASKIN", "Baskin FC Failover 0", "Fail over",
    "Baskin Robbins Front Counter Failover", "BR FC 1 failover",
    "Front Counter Baskin Failover 1", "Baskin FCF", "FCB Failover",
    "FC Failover BR", "Baskin FC 1 Failover", "BR FC FO",
    "Front Counter Failover\xa0 0", "FCB Failover 0", "FC BR 0 Failover",
    "FC BR - 1 - Failover", "FC Baskin Failover 1", "BR Counter Failover",
    "Front Counter BR failover", "Failover Front Counter Baskin",
    "Front Counter Baskin- Failover", "FC 1 Baskin Failover",
    "Baskins Failover", "Baskins Robbins Failover", "FC 2 Failvoer",
    "FC ! Failover", "Baskin Robbins FC FO",
    "Front Counter 1 BR Failover", "Front Counter Failover BR 0",
    "Baskin Robbins FC FA", "Baskin Robbin FC failover",
    "1st Floor Baskin Failover", "BR FC Failover",
    "Front Counter Baskin Robbins Failover", "BR 1 Failover",
    "Front Counter Baskin 1 Failover", "Front counter Baskin 0 failover",
    "FC Baskin Failover 0", "FC BR 1 Failover",
    "Front Counter Baskin Failover\xa0 FCB Failover 0", "FC BR Failover",
    "Baskin FC 0 Failover", "Baskin 1 Failover",
    "Baskin Front Counter Failover 1", "FC\xa0 Failover 1",
    "Front Counter Baskin Robbins Standalone Failover",
    "Front Counter Baskin\xa0 failover", "FC BR FailOver 0",
    "FC Baskin - Failover", "Promo Failover 1", "OSB Failover",
    "OSB Failover 1", "OBS Failover 1", "Walk Up Window - 1 Failover",
    "Walk up Failover"
]

for value in test_values:
    result = standardize_failover(value)
    print(f"Input: '{value}' -> Output: '{result}'")