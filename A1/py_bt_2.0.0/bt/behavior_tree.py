# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the behavior tree
import bt_library as btl

import bt as bt

# sequence for battery < 30 and the charging process
battery_seq = bt.Sequence(
    [
        bt.BatteryLessThan30(),
        bt.FindHome(),
        bt.GoHome(),
        bt.Dock()

    ]
)
# spot cleaning condition
spot_seq = bt.Sequence(
    [
        bt.SpotCleaning(),
        btl.Timer(20, bt.CleanSpot()),
        bt.DoneSpot()
    ]
)
# dusty sensor second sequence
dusty_seq2 = bt.Sequence(
    [
        bt.DustySpot(),
        btl.Timer(35, bt.CleanSpot()),
        bt.AlwaysFail()
    ]
)
# dusty sensor priority
dusty_priority = bt.Priority(
    [
        dusty_seq2,
        bt.CleanFloor()
    ]
)
# dusty spot first sequence
dusty_seq1 = bt.Sequence(
    [
        dusty_priority,
        bt.DoneGeneral()

    ]
)
# general cleaning sequence
gen_seq = bt.Sequence(
    [
        bt.GeneralCleaning(),
        dusty_seq1

    ]
)
# selection for cleaning
clean_selec = bt.Selection(
    [
        spot_seq,
        gen_seq
    ]
)
# priority root of the btree
tree_root = bt.Priority(
    [
        battery_seq,
        clean_selec,
        bt.DoNothing()

    ]
)
