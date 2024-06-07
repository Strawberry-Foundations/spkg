use crate::spinners::utils::spinner_data::SpinnerData;
use lazy_static::lazy_static;
use maplit::{self, hashmap};
use std::collections::HashMap;

lazy_static! {
    pub static ref SPINNERS: HashMap<String, SpinnerData> = {
        hashmap! {
              "Dots".into() => SpinnerData {frames: vec![
          "⠋",
          "⠙",
          "⠹",
          "⠸",
          "⠼",
          "⠴",
          "⠦",
          "⠧",
          "⠇",
          "⠏"
        ], interval: 80},
        "Dots2".into() => SpinnerData {frames: vec![
          "⣾",
          "⣽",
          "⣻",
          "⢿",
          "⡿",
          "⣟",
          "⣯",
          "⣷"
        ], interval: 80},
        "Dots3".into() => SpinnerData {frames: vec![
          "⠋",
          "⠙",
          "⠚",
          "⠞",
          "⠖",
          "⠦",
          "⠴",
          "⠲",
          "⠳",
          "⠓"
        ], interval: 80},
        "Dots4".into() => SpinnerData {frames: vec![
          "⠄",
          "⠆",
          "⠇",
          "⠋",
          "⠙",
          "⠸",
          "⠰",
          "⠠",
          "⠰",
          "⠸",
          "⠙",
          "⠋",
          "⠇",
          "⠆"
        ], interval: 80},
        "Dots5".into() => SpinnerData {frames: vec![
          "⠋",
          "⠙",
          "⠚",
          "⠒",
          "⠂",
          "⠂",
          "⠒",
          "⠲",
          "⠴",
          "⠦",
          "⠖",
          "⠒",
          "⠐",
          "⠐",
          "⠒",
          "⠓",
          "⠋"
        ], interval: 80},
        "Dots6".into() => SpinnerData {frames: vec![
          "⠁",
          "⠉",
          "⠙",
          "⠚",
          "⠒",
          "⠂",
          "⠂",
          "⠒",
          "⠲",
          "⠴",
          "⠤",
          "⠄",
          "⠄",
          "⠤",
          "⠴",
          "⠲",
          "⠒",
          "⠂",
          "⠂",
          "⠒",
          "⠚",
          "⠙",
          "⠉",
          "⠁"
        ], interval: 80},
        "Dots7".into() => SpinnerData {frames: vec![
          "⠈",
          "⠉",
          "⠋",
          "⠓",
          "⠒",
          "⠐",
          "⠐",
          "⠒",
          "⠖",
          "⠦",
          "⠤",
          "⠠",
          "⠠",
          "⠤",
          "⠦",
          "⠖",
          "⠒",
          "⠐",
          "⠐",
          "⠒",
          "⠓",
          "⠋",
          "⠉",
          "⠈"
        ], interval: 80},
        "Dots8".into() => SpinnerData {frames: vec![
          "⠁",
          "⠁",
          "⠉",
          "⠙",
          "⠚",
          "⠒",
          "⠂",
          "⠂",
          "⠒",
          "⠲",
          "⠴",
          "⠤",
          "⠄",
          "⠄",
          "⠤",
          "⠠",
          "⠠",
          "⠤",
          "⠦",
          "⠖",
          "⠒",
          "⠐",
          "⠐",
          "⠒",
          "⠓",
          "⠋",
          "⠉",
          "⠈",
          "⠈"
        ], interval: 80},
        "Dots9".into() => SpinnerData {frames: vec![
          "⢹",
          "⢺",
          "⢼",
          "⣸",
          "⣇",
          "⡧",
          "⡗",
          "⡏"
        ], interval: 80},
        "Dots10".into() => SpinnerData {frames: vec![
          "⢄",
          "⢂",
          "⢁",
          "⡁",
          "⡈",
          "⡐",
          "⡠"
        ], interval: 80},
        "Dots11".into() => SpinnerData {frames: vec![
          "⠁",
          "⠂",
          "⠄",
          "⡀",
          "⢀",
          "⠠",
          "⠐",
          "⠈"
        ], interval: 100},
        "Dots12".into() => SpinnerData {frames: vec![
          "⢀⠀",
          "⡀⠀",
          "⠄⠀",
          "⢂⠀",
          "⡂⠀",
          "⠅⠀",
          "⢃⠀",
          "⡃⠀",
          "⠍⠀",
          "⢋⠀",
          "⡋⠀",
          "⠍⠁",
          "⢋⠁",
          "⡋⠁",
          "⠍⠉",
          "⠋⠉",
          "⠋⠉",
          "⠉⠙",
          "⠉⠙",
          "⠉⠩",
          "⠈⢙",
          "⠈⡙",
          "⢈⠩",
          "⡀⢙",
          "⠄⡙",
          "⢂⠩",
          "⡂⢘",
          "⠅⡘",
          "⢃⠨",
          "⡃⢐",
          "⠍⡐",
          "⢋⠠",
          "⡋⢀",
          "⠍⡁",
          "⢋⠁",
          "⡋⠁",
          "⠍⠉",
          "⠋⠉",
          "⠋⠉",
          "⠉⠙",
          "⠉⠙",
          "⠉⠩",
          "⠈⢙",
          "⠈⡙",
          "⠈⠩",
          "⠀⢙",
          "⠀⡙",
          "⠀⠩",
          "⠀⢘",
          "⠀⡘",
          "⠀⠨",
          "⠀⢐",
          "⠀⡐",
          "⠀⠠",
          "⠀⢀",
          "⠀⡀"
        ], interval: 80},
        "Dots8Bit".into() => SpinnerData {frames: vec![
          "⠀",
          "⠁",
          "⠂",
          "⠃",
          "⠄",
          "⠅",
          "⠆",
          "⠇",
          "⡀",
          "⡁",
          "⡂",
          "⡃",
          "⡄",
          "⡅",
          "⡆",
          "⡇",
          "⠈",
          "⠉",
          "⠊",
          "⠋",
          "⠌",
          "⠍",
          "⠎",
          "⠏",
          "⡈",
          "⡉",
          "⡊",
          "⡋",
          "⡌",
          "⡍",
          "⡎",
          "⡏",
          "⠐",
          "⠑",
          "⠒",
          "⠓",
          "⠔",
          "⠕",
          "⠖",
          "⠗",
          "⡐",
          "⡑",
          "⡒",
          "⡓",
          "⡔",
          "⡕",
          "⡖",
          "⡗",
          "⠘",
          "⠙",
          "⠚",
          "⠛",
          "⠜",
          "⠝",
          "⠞",
          "⠟",
          "⡘",
          "⡙",
          "⡚",
          "⡛",
          "⡜",
          "⡝",
          "⡞",
          "⡟",
          "⠠",
          "⠡",
          "⠢",
          "⠣",
          "⠤",
          "⠥",
          "⠦",
          "⠧",
          "⡠",
          "⡡",
          "⡢",
          "⡣",
          "⡤",
          "⡥",
          "⡦",
          "⡧",
          "⠨",
          "⠩",
          "⠪",
          "⠫",
          "⠬",
          "⠭",
          "⠮",
          "⠯",
          "⡨",
          "⡩",
          "⡪",
          "⡫",
          "⡬",
          "⡭",
          "⡮",
          "⡯",
          "⠰",
          "⠱",
          "⠲",
          "⠳",
          "⠴",
          "⠵",
          "⠶",
          "⠷",
          "⡰",
          "⡱",
          "⡲",
          "⡳",
          "⡴",
          "⡵",
          "⡶",
          "⡷",
          "⠸",
          "⠹",
          "⠺",
          "⠻",
          "⠼",
          "⠽",
          "⠾",
          "⠿",
          "⡸",
          "⡹",
          "⡺",
          "⡻",
          "⡼",
          "⡽",
          "⡾",
          "⡿",
          "⢀",
          "⢁",
          "⢂",
          "⢃",
          "⢄",
          "⢅",
          "⢆",
          "⢇",
          "⣀",
          "⣁",
          "⣂",
          "⣃",
          "⣄",
          "⣅",
          "⣆",
          "⣇",
          "⢈",
          "⢉",
          "⢊",
          "⢋",
          "⢌",
          "⢍",
          "⢎",
          "⢏",
          "⣈",
          "⣉",
          "⣊",
          "⣋",
          "⣌",
          "⣍",
          "⣎",
          "⣏",
          "⢐",
          "⢑",
          "⢒",
          "⢓",
          "⢔",
          "⢕",
          "⢖",
          "⢗",
          "⣐",
          "⣑",
          "⣒",
          "⣓",
          "⣔",
          "⣕",
          "⣖",
          "⣗",
          "⢘",
          "⢙",
          "⢚",
          "⢛",
          "⢜",
          "⢝",
          "⢞",
          "⢟",
          "⣘",
          "⣙",
          "⣚",
          "⣛",
          "⣜",
          "⣝",
          "⣞",
          "⣟",
          "⢠",
          "⢡",
          "⢢",
          "⢣",
          "⢤",
          "⢥",
          "⢦",
          "⢧",
          "⣠",
          "⣡",
          "⣢",
          "⣣",
          "⣤",
          "⣥",
          "⣦",
          "⣧",
          "⢨",
          "⢩",
          "⢪",
          "⢫",
          "⢬",
          "⢭",
          "⢮",
          "⢯",
          "⣨",
          "⣩",
          "⣪",
          "⣫",
          "⣬",
          "⣭",
          "⣮",
          "⣯",
          "⢰",
          "⢱",
          "⢲",
          "⢳",
          "⢴",
          "⢵",
          "⢶",
          "⢷",
          "⣰",
          "⣱",
          "⣲",
          "⣳",
          "⣴",
          "⣵",
          "⣶",
          "⣷",
          "⢸",
          "⢹",
          "⢺",
          "⢻",
          "⢼",
          "⢽",
          "⢾",
          "⢿",
          "⣸",
          "⣹",
          "⣺",
          "⣻",
          "⣼",
          "⣽",
          "⣾",
          "⣿"
        ], interval: 80},
        "Line".into() => SpinnerData {frames: vec![
          "\x1b[32m\x1b[1m - \x1b[0m",
          "\x1b[32m\x1b[1m \\ \x1b[0m",
          "\x1b[32m\x1b[1m | \x1b[0m",
          "\x1b[32m\x1b[1m / \x1b[0m"
        ], interval: 130},
        "Line2".into() => SpinnerData {frames: vec![
          "⠂",
          "-",
          "–",
          "—",
          "–",
          "-"
        ], interval: 100},
        "Pipe".into() => SpinnerData {frames: vec![
          "┤",
          "┘",
          "┴",
          "└",
          "├",
          "┌",
          "┬",
          "┐"
        ], interval: 100},
        "SimpleDots".into() => SpinnerData {frames: vec![
          ".  ",
          ".. ",
          "...",
          "   "
        ], interval: 400},
        "SimpleDotsScrolling".into() => SpinnerData {frames: vec![
          ".  ",
          ".. ",
          "...",
          " ..",
          "  .",
          "   "
        ], interval: 200},
        "Star".into() => SpinnerData {frames: vec![
          "✶",
          "✸",
          "✹",
          "✺",
          "✹",
          "✷"
        ], interval: 70},
        "Star2".into() => SpinnerData {frames: vec![
          "+",
          "x",
          "*"
        ], interval: 80},
        "Flip".into() => SpinnerData {frames: vec![
          "_",
          "_",
          "_",
          "-",
          "`",
          "`",
          "'",
          "´",
          "-",
          "_",
          "_",
          "_"
        ], interval: 70},
        "Hamburger".into() => SpinnerData {frames: vec![
          "☱",
          "☲",
          "☴"
        ], interval: 100},
        "GrowVertical".into() => SpinnerData {frames: vec![
          "▁",
          "▃",
          "▄",
          "▅",
          "▆",
          "▇",
          "▆",
          "▅",
          "▄",
          "▃"
        ], interval: 120},
        "GrowHorizontal".into() => SpinnerData {frames: vec![
          "▏",
          "▎",
          "▍",
          "▌",
          "▋",
          "▊",
          "▉",
          "▊",
          "▋",
          "▌",
          "▍",
          "▎"
        ], interval: 120},
        "Balloon".into() => SpinnerData {frames: vec![
          " ",
          ".",
          "o",
          "O",
          "@",
          "*",
          " "
        ], interval: 140},
        "Balloon2".into() => SpinnerData {frames: vec![
          ".",
          "o",
          "O",
          "°",
          "O",
          "o",
          "."
        ], interval: 120},
        "Noise".into() => SpinnerData {frames: vec![
          "▓",
          "▒",
          "░"
        ], interval: 100},
        "Bounce".into() => SpinnerData {frames: vec![
          "⠁",
          "⠂",
          "⠄",
          "⠂"
        ], interval: 120},
        "BoxBounce".into() => SpinnerData {frames: vec![
          "▖",
          "▘",
          "▝",
          "▗"
        ], interval: 120},
        "BoxBounce2".into() => SpinnerData {frames: vec![
          "▌",
          "▀",
          "▐",
          "▄"
        ], interval: 100},
        "Triangle".into() => SpinnerData {frames: vec![
          "◢",
          "◣",
          "◤",
          "◥"
        ], interval: 50},
        "Arc".into() => SpinnerData {frames: vec![
          "◜",
          "◠",
          "◝",
          "◞",
          "◡",
          "◟"
        ], interval: 100},
        "Circle".into() => SpinnerData {frames: vec![
          "◡",
          "⊙",
          "◠"
        ], interval: 120},
        "SquareCorners".into() => SpinnerData {frames: vec![
          "◰",
          "◳",
          "◲",
          "◱"
        ], interval: 180},
        "CircleQuarters".into() => SpinnerData {frames: vec![
          "◴",
          "◷",
          "◶",
          "◵"
        ], interval: 120},
        "CircleHalves".into() => SpinnerData {frames: vec![
          "◐",
          "◓",
          "◑",
          "◒"
        ], interval: 50},
        "Squish".into() => SpinnerData {frames: vec![
          "╫",
          "╪"
        ], interval: 100},
        "Toggle".into() => SpinnerData {frames: vec![
          "⊶",
          "⊷"
        ], interval: 250},
        "Toggle2".into() => SpinnerData {frames: vec![
          "▫",
          "▪"
        ], interval: 80},
        "Toggle3".into() => SpinnerData {frames: vec![
          "□",
          "■"
        ], interval: 120},
        "Toggle4".into() => SpinnerData {frames: vec![
          "■",
          "□",
          "▪",
          "▫"
        ], interval: 100},
        "Toggle5".into() => SpinnerData {frames: vec![
          "▮",
          "▯"
        ], interval: 100},
        "Toggle6".into() => SpinnerData {frames: vec![
          "ဝ",
          "၀"
        ], interval: 300},
        "Toggle7".into() => SpinnerData {frames: vec![
          "⦾",
          "⦿"
        ], interval: 80},
        "Toggle8".into() => SpinnerData {frames: vec![
          "◍",
          "◌"
        ], interval: 100},
        "Toggle9".into() => SpinnerData {frames: vec![
          "◉",
          "◎"
        ], interval: 100},
        "Toggle10".into() => SpinnerData {frames: vec![
          "㊂",
          "㊀",
          "㊁"
        ], interval: 100},
        "Toggle11".into() => SpinnerData {frames: vec![
          "⧇",
          "⧆"
        ], interval: 50},
        "Toggle12".into() => SpinnerData {frames: vec![
          "☗",
          "☖"
        ], interval: 120},
        "Toggle13".into() => SpinnerData {frames: vec![
          "=",
          "*",
          "-"
        ], interval: 80},
        "Arrow".into() => SpinnerData {frames: vec![
          "←",
          "↖",
          "↑",
          "↗",
          "→",
          "↘",
          "↓",
          "↙"
        ], interval: 100},
        "Arrow2".into() => SpinnerData {frames: vec![
          "⬆️ ",
          "↗️ ",
          "➡️ ",
          "↘️ ",
          "⬇️ ",
          "↙️ ",
          "⬅️ ",
          "↖️ "
        ], interval: 80},
        "Arrow3".into() => SpinnerData {frames: vec![
          "▹▹▹▹▹",
          "▸▹▹▹▹",
          "▹▸▹▹▹",
          "▹▹▸▹▹",
          "▹▹▹▸▹",
          "▹▹▹▹▸"
        ], interval: 120},
        "BouncingBar".into() => SpinnerData {frames: vec![
          "[    ]",
          "[=   ]",
          "[==  ]",
          "[=== ]",
          "[ ===]",
          "[  ==]",
          "[   =]",
          "[    ]",
          "[   =]",
          "[  ==]",
          "[ ===]",
          "[====]",
          "[=== ]",
          "[==  ]",
          "[=   ]"
        ], interval: 80},
        "BouncingBall".into() => SpinnerData {frames: vec![
          "( ●    )",
          "(  ●   )",
          "(   ●  )",
          "(    ● )",
          "(     ●)",
          "(    ● )",
          "(   ●  )",
          "(  ●   )",
          "( ●    )",
          "(●     )"
        ], interval: 80},
        "Smiley".into() => SpinnerData {frames: vec![
          "😄 ",
          "😝 "
        ], interval: 200},
        "Monkey".into() => SpinnerData {frames: vec![
          "🙈 ",
          "🙈 ",
          "🙉 ",
          "🙊 "
        ], interval: 300},
        "Hearts".into() => SpinnerData {frames: vec![
          "💛 ",
          "💙 ",
          "💜 ",
          "💚 ",
          "❤️ "
        ], interval: 100},
        "Clock".into() => SpinnerData {frames: vec![
          "🕛 ",
          "🕐 ",
          "🕑 ",
          "🕒 ",
          "🕓 ",
          "🕔 ",
          "🕕 ",
          "🕖 ",
          "🕗 ",
          "🕘 ",
          "🕙 ",
          "🕚 "
        ], interval: 100},
        "Earth".into() => SpinnerData {frames: vec![
          "🌍 ",
          "🌎 ",
          "🌏 "
        ], interval: 180},
        "Material".into() => SpinnerData {frames: vec![
          "█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "███▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "████▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "██████▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "██████▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "███████▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "████████▁▁▁▁▁▁▁▁▁▁▁▁",
          "█████████▁▁▁▁▁▁▁▁▁▁▁",
          "█████████▁▁▁▁▁▁▁▁▁▁▁",
          "██████████▁▁▁▁▁▁▁▁▁▁",
          "███████████▁▁▁▁▁▁▁▁▁",
          "█████████████▁▁▁▁▁▁▁",
          "██████████████▁▁▁▁▁▁",
          "██████████████▁▁▁▁▁▁",
          "▁██████████████▁▁▁▁▁",
          "▁██████████████▁▁▁▁▁",
          "▁██████████████▁▁▁▁▁",
          "▁▁██████████████▁▁▁▁",
          "▁▁▁██████████████▁▁▁",
          "▁▁▁▁█████████████▁▁▁",
          "▁▁▁▁██████████████▁▁",
          "▁▁▁▁██████████████▁▁",
          "▁▁▁▁▁██████████████▁",
          "▁▁▁▁▁██████████████▁",
          "▁▁▁▁▁██████████████▁",
          "▁▁▁▁▁▁██████████████",
          "▁▁▁▁▁▁██████████████",
          "▁▁▁▁▁▁▁█████████████",
          "▁▁▁▁▁▁▁█████████████",
          "▁▁▁▁▁▁▁▁████████████",
          "▁▁▁▁▁▁▁▁████████████",
          "▁▁▁▁▁▁▁▁▁███████████",
          "▁▁▁▁▁▁▁▁▁███████████",
          "▁▁▁▁▁▁▁▁▁▁██████████",
          "▁▁▁▁▁▁▁▁▁▁██████████",
          "▁▁▁▁▁▁▁▁▁▁▁▁████████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁███████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁██████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█████",
          "█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
          "██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
          "██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
          "███▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
          "████▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
          "█████▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
          "█████▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
          "██████▁▁▁▁▁▁▁▁▁▁▁▁▁█",
          "████████▁▁▁▁▁▁▁▁▁▁▁▁",
          "█████████▁▁▁▁▁▁▁▁▁▁▁",
          "█████████▁▁▁▁▁▁▁▁▁▁▁",
          "█████████▁▁▁▁▁▁▁▁▁▁▁",
          "█████████▁▁▁▁▁▁▁▁▁▁▁",
          "███████████▁▁▁▁▁▁▁▁▁",
          "████████████▁▁▁▁▁▁▁▁",
          "████████████▁▁▁▁▁▁▁▁",
          "██████████████▁▁▁▁▁▁",
          "██████████████▁▁▁▁▁▁",
          "▁██████████████▁▁▁▁▁",
          "▁██████████████▁▁▁▁▁",
          "▁▁▁█████████████▁▁▁▁",
          "▁▁▁▁▁████████████▁▁▁",
          "▁▁▁▁▁████████████▁▁▁",
          "▁▁▁▁▁▁███████████▁▁▁",
          "▁▁▁▁▁▁▁▁█████████▁▁▁",
          "▁▁▁▁▁▁▁▁█████████▁▁▁",
          "▁▁▁▁▁▁▁▁▁█████████▁▁",
          "▁▁▁▁▁▁▁▁▁█████████▁▁",
          "▁▁▁▁▁▁▁▁▁▁█████████▁",
          "▁▁▁▁▁▁▁▁▁▁▁████████▁",
          "▁▁▁▁▁▁▁▁▁▁▁████████▁",
          "▁▁▁▁▁▁▁▁▁▁▁▁███████▁",
          "▁▁▁▁▁▁▁▁▁▁▁▁███████▁",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁███████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁███████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
          "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁"
        ], interval: 17},
        "Moon".into() => SpinnerData {frames: vec![
          "🌑 ",
          "🌒 ",
          "🌓 ",
          "🌔 ",
          "🌕 ",
          "🌖 ",
          "🌗 ",
          "🌘 "
        ], interval: 80},
        "Runner".into() => SpinnerData {frames: vec![
          "🚶 ",
          "🏃 "
        ], interval: 140},
        "Pong".into() => SpinnerData {frames: vec![
          "▐⠂       ▌",
          "▐⠈       ▌",
          "▐ ⠂      ▌",
          "▐ ⠠      ▌",
          "▐  ⡀     ▌",
          "▐  ⠠     ▌",
          "▐   ⠂    ▌",
          "▐   ⠈    ▌",
          "▐    ⠂   ▌",
          "▐    ⠠   ▌",
          "▐     ⡀  ▌",
          "▐     ⠠  ▌",
          "▐      ⠂ ▌",
          "▐      ⠈ ▌",
          "▐       ⠂▌",
          "▐       ⠠▌",
          "▐       ⡀▌",
          "▐      ⠠ ▌",
          "▐      ⠂ ▌",
          "▐     ⠈  ▌",
          "▐     ⠂  ▌",
          "▐    ⠠   ▌",
          "▐    ⡀   ▌",
          "▐   ⠠    ▌",
          "▐   ⠂    ▌",
          "▐  ⠈     ▌",
          "▐  ⠂     ▌",
          "▐ ⠠      ▌",
          "▐ ⡀      ▌",
          "▐⠠       ▌"
        ], interval: 80},
        "Shark".into() => SpinnerData {frames: vec![
          "▐|\\____________▌",
          "▐_|\\___________▌",
          "▐__|\\__________▌",
          "▐___|\\_________▌",
          "▐____|\\________▌",
          "▐_____|\\_______▌",
          "▐______|\\______▌",
          "▐_______|\\_____▌",
          "▐________|\\____▌",
          "▐_________|\\___▌",
          "▐__________|\\__▌",
          "▐___________|\\_▌",
          "▐____________|\\▌",
          "▐____________/|▌",
          "▐___________/|_▌",
          "▐__________/|__▌",
          "▐_________/|___▌",
          "▐________/|____▌",
          "▐_______/|_____▌",
          "▐______/|______▌",
          "▐_____/|_______▌",
          "▐____/|________▌",
          "▐___/|_________▌",
          "▐__/|__________▌",
          "▐_/|___________▌",
          "▐/|____________▌"
        ], interval: 120},
        "Dqpb".into() => SpinnerData {frames: vec![
          "d",
          "q",
          "p",
          "b"
        ], interval: 100},
        "Weather".into() => SpinnerData {frames: vec![
          "☀️ ",
          "☀️ ",
          "☀️ ",
          "🌤 ",
          "⛅️ ",
          "🌥 ",
          "☁️ ",
          "🌧 ",
          "🌨 ",
          "🌧 ",
          "🌨 ",
          "🌧 ",
          "🌨 ",
          "⛈ ",
          "🌨 ",
          "🌧 ",
          "🌨 ",
          "☁️ ",
          "🌥 ",
          "⛅️ ",
          "🌤 ",
          "☀️ ",
          "☀️ "
        ], interval: 100},
        "Christmas".into() => SpinnerData {frames: vec![
          "🌲",
          "🎄"
        ], interval: 400},
        "Grenade".into() => SpinnerData {frames: vec![
          "،  ",
          "′  ",
          " ´ ",
          " ‾ ",
          "  ⸌",
          "  ⸊",
          "  |",
          "  ⁎",
          "  ⁕",
          " ෴ ",
          "  ⁓",
          "   ",
          "   ",
          "   "
        ], interval: 80},
        "Point".into() => SpinnerData {frames: vec![
          "∙∙∙",
          "●∙∙",
          "∙●∙",
          "∙∙●",
          "∙∙∙"
        ], interval: 125},
        "Layer".into() => SpinnerData {frames: vec![
          "-",
          "=",
          "≡"
        ], interval: 150},
        "BetaWave".into() => SpinnerData {frames: vec![
          "ρββββββ",
          "βρβββββ",
          "ββρββββ",
          "βββρβββ",
          "ββββρββ",
          "βββββρβ",
          "ββββββρ"
        ], interval: 80},
        "FingerDance".into() => SpinnerData {frames: vec![
          "🤘 ",
          "🤟 ",
          "🖖 ",
          "✋ ",
          "🤚 ",
          "👆 "
        ], interval: 160},
        "FistBump".into() => SpinnerData {frames: vec![
          "🤜　　　　🤛 ",
          "🤜　　　　🤛 ",
          "🤜　　　　🤛 ",
          "　🤜　　🤛　 ",
          "　　🤜🤛　　 ",
          "　🤜✨🤛　　 ",
          "🤜　✨　🤛　 "
        ], interval: 80},
        "SoccerHeader".into() => SpinnerData {frames: vec![
          " 🧑⚽️       🧑 ",
          "🧑  ⚽️      🧑 ",
          "🧑   ⚽️     🧑 ",
          "🧑    ⚽️    🧑 ",
          "🧑     ⚽️   🧑 ",
          "🧑      ⚽️  🧑 ",
          "🧑       ⚽️🧑  ",
          "🧑      ⚽️  🧑 ",
          "🧑     ⚽️   🧑 ",
          "🧑    ⚽️    🧑 ",
          "🧑   ⚽️     🧑 ",
          "🧑  ⚽️      🧑 "
        ], interval: 80},
        "Mindblown".into() => SpinnerData {frames: vec![
          "😐 ",
          "😐 ",
          "😮 ",
          "😮 ",
          "😦 ",
          "😦 ",
          "😧 ",
          "😧 ",
          "🤯 ",
          "💥 ",
          "✨ ",
          "　 ",
          "　 ",
          "　 "
        ], interval: 160},
        "Speaker".into() => SpinnerData {frames: vec![
          "🔈 ",
          "🔉 ",
          "🔊 ",
          "🔉 "
        ], interval: 160},
        "OrangePulse".into() => SpinnerData {frames: vec![
          "🔸 ",
          "🔶 ",
          "🟠 ",
          "🟠 ",
          "🔶 "
        ], interval: 100},
        "BluePulse".into() => SpinnerData {frames: vec![
          "🔹 ",
          "🔷 ",
          "🔵 ",
          "🔵 ",
          "🔷 "
        ], interval: 100},
        "OrangeBluePulse".into() => SpinnerData {frames: vec![
          "🔸 ",
          "🔶 ",
          "🟠 ",
          "🟠 ",
          "🔶 ",
          "🔹 ",
          "🔷 ",
          "🔵 ",
          "🔵 ",
          "🔷 "
        ], interval: 100},
        "TimeTravel".into() => SpinnerData {frames: vec![
          "🕛 ",
          "🕚 ",
          "🕙 ",
          "🕘 ",
          "🕗 ",
          "🕖 ",
          "🕕 ",
          "🕔 ",
          "🕓 ",
          "🕒 ",
          "🕑 ",
          "🕐 "
        ], interval: 100},
        "Aesthetic".into() => SpinnerData {frames: vec![
          "▰▱▱▱▱▱▱",
          "▰▰▱▱▱▱▱",
          "▰▰▰▱▱▱▱",
          "▰▰▰▰▱▱▱",
          "▰▰▰▰▰▱▱",
          "▰▰▰▰▰▰▱",
          "▰▰▰▰▰▰▰",
          "▰▱▱▱▱▱▱"
        ], interval: 80}
            }
    };
}
