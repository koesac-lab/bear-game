# data.py
#
# Canonical data model for the Bear Game.
#
# The application treats these IDs as immutable. Do not derive IDs from display
# names: names can change, while IDs are used by brackets, votes, cached assets,
# and the API.

from __future__ import annotations

from typing import Any

MEDIA_SOURCES: dict[str, dict[str, str]] = {
    "explore": {
        "label": "Explore.org",
        "url": "https://explore.org/livecams/brown-bears/brown-bear-salmon-cam-brooks-falls",
    },
    "popular_science": {
        "label": "Popular Science",
        "url": "https://www.popsci.com/environment/fat-bear-week/",
    },
}

# Each asset key is deliberately stable and source-specific:
#
#   b132-explore  -> full-width “before”/matchup image
#   b132-card     -> square-ish fact card image
#
# `before_url` and `card_url` are source records, not browser-facing endpoints.
# cache_photos.py downloads them into static/media/ and server.py exposes only
# local /media/<asset-key> routes.
#
# If an upstream image moves, update its URL while retaining the cache key. The
# cache refresh process will replace the local file without changing a bracket,
# a client payload, or any saved vote.

BEARS: list[dict[str, Any]] = [
    {
        "id": "b132",
        "name": "Chunk",
        "tagline": "A dominant, broad-shouldered Brooks River regular.",
        "fact": (
            "Chunk is one of Katmai’s best-known adult males and is recognized "
            "for his exceptionally large frame and steady fishing style."
        ),
        "before_caption": "Chunk fishing at Brooks Falls.",
        "card_caption": "Chunk in peak Fat Bear Week condition.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2020/09/brown-bear-chunk-brooks-falls.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-chunk.jpg",
        "before_key": "b132-explore",
        "card_key": "b132-card",
        "seed": 1,
    },
    {
        "id": "b128",
        "name": "Grazer",
        "tagline": "A formidable female famous for raising successful cubs.",
        "fact": (
            "Grazer is a highly recognizable adult female whose confidence and "
            "aggressive defense of feeding space make her a fan favorite."
        ),
        "before_caption": "Grazer working the Brooks River.",
        "card_caption": "Grazer during a late-summer salmon run.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2020/09/brown-bear-grazer-brooks-falls.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-grazer.jpg",
        "before_key": "b128-explore",
        "card_key": "b128-card",
        "seed": 2,
    },
    {
        "id": "b164",
        "name": "Shenanigans",
        "tagline": "A big, familiar male with an expressive presence.",
        "fact": (
            "Shenanigans is a mature male whose size and demeanor make him easy "
            "to spot among the bears that return to Brooks River season after season."
        ),
        "before_caption": "Shenanigans scanning the river.",
        "card_caption": "Shenanigans after a productive fishing day.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2021/09/brown-bear-shenanigans-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-shenanigans.jpg",
        "before_key": "b164-explore",
        "card_key": "b164-card",
        "seed": 3,
    },
    {
        "id": "b435",
        "name": "Holly",
        "tagline": "A skilled mother and longtime Katmai favorite.",
        "fact": (
            "Holly is celebrated for her calm, efficient fishing and for the "
            "care she gives her cubs while navigating a crowded river."
        ),
        "before_caption": "Holly moving along Brooks River.",
        "card_caption": "Holly in her autumn coat.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2020/09/brown-bear-holly-brooks-river.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-holly.jpg",
        "before_key": "b435-explore",
        "card_key": "b435-card",
        "seed": 4,
    },
    {
        "id": "b32",
        "name": "Chunky",
        "tagline": "A compact powerhouse built for a salmon-rich season.",
        "fact": (
            "Chunky’s robust build reflects the extraordinary seasonal calorie "
            "intake that helps Katmai bears survive winter hibernation."
        ),
        "before_caption": "Chunky at the edge of the current.",
        "card_caption": "Chunky in late-season condition.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2021/08/brown-bear-chunky-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-chunky.jpg",
        "before_key": "b32-explore",
        "card_key": "b32-card",
        "seed": 5,
    },
    {
        "id": "b480",
        "name": "Otis",
        "tagline": "A patient fishing specialist and beloved veteran.",
        "fact": (
            "Otis is famous for his efficient sit-and-wait technique: he lets "
            "salmon come to him rather than expending energy chasing every fish."
        ),
        "before_caption": "Otis using his patient fishing technique.",
        "card_caption": "Otis at Brooks Falls.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2020/09/brown-bear-otis-brooks-falls.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-otis.jpg",
        "before_key": "b480-explore",
        "card_key": "b480-card",
        "seed": 6,
    },
    {
        "id": "b747",
        "name": "Bear 747",
        "tagline": "The famously enormous champion of Brooks River.",
        "fact": (
            "Bear 747 is known for an immense body size that allows him to "
            "dominate prime fishing spots and store exceptional winter reserves."
        ),
        "before_caption": "Bear 747 in the Brooks River.",
        "card_caption": "Bear 747 in heavyweight autumn form.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2020/09/brown-bear-747-brooks-falls.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-747.jpg",
        "before_key": "b747-explore",
        "card_key": "b747-card",
        "seed": 7,
    },
    {
        "id": "b151",
        "name": "Walker",
        "tagline": "A large male with a deliberate, confident stride.",
        "fact": (
            "Walker is a mature male often seen moving between fishing locations "
            "as salmon availability changes throughout the season."
        ),
        "before_caption": "Walker along a Katmai riverbank.",
        "card_caption": "Walker after the summer salmon run.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2021/09/brown-bear-walker-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-walker.jpg",
        "before_key": "b151-explore",
        "card_key": "b151-card",
        "seed": 8,
    },
    {
        "id": "b410",
        "name": "Jr.",
        "tagline": "A younger bear learning the rhythms of Brooks River.",
        "fact": (
            "Jr. represents the next generation of bears that gain experience "
            "by observing older fishers and testing the river’s changing currents."
        ),
        "before_caption": "Jr. studying the waterline.",
        "card_caption": "Jr. during the fall feeding season.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2021/08/brown-bear-jr-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-jr.jpg",
        "before_key": "b410-explore",
        "card_key": "b410-card",
        "seed": 9,
    },
    {
        "id": "b1282",
        "name": "Grazer's Cub",
        "tagline": "A young bear learning from one of Katmai’s best mothers.",
        "fact": (
            "Cubs spend several years with their mother, learning where to fish, "
            "how to avoid danger, and how to compete for salmon."
        ),
        "before_caption": "Grazer’s cub near the water.",
        "card_caption": "A young Katmai bear in autumn.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2022/08/brown-bear-grazers-cub-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-cub.jpg",
        "before_key": "b1282-explore",
        "card_key": "b1282-card",
        "seed": 10,
    },
    {
        "id": "b402",
        "name": "Donut",
        "tagline": "A round, resourceful adult female.",
        "fact": (
            "Donut’s name reflects the memorable appearance that makes individual "
            "identification possible in the annual Katmai bear roster."
        ),
        "before_caption": "Donut crossing shallow water.",
        "card_caption": "Donut during salmon season.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2021/09/brown-bear-donut-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-donut.jpg",
        "before_key": "b402-explore",
        "card_key": "b402-card",
        "seed": 11,
    },
    {
        "id": "b901",
        "name": "Aunty",
        "tagline": "An experienced adult female with river savvy.",
        "fact": (
            "Aunty is part of the community of individually identified bears "
            "whose long-term observations help tell Katmai’s seasonal story."
        ),
        "before_caption": "Aunty at a quiet river bend.",
        "card_caption": "Aunty in late summer.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2022/09/brown-bear-aunty-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-aunty.jpg",
        "before_key": "b901-explore",
        "card_key": "b901-card",
        "seed": 12,
    },
    {
        "id": "b32a",
        "name": "Divot",
        "tagline": "A recognizable bear with a distinctive facial profile.",
        "fact": (
            "Natural markings, size, gait, and facial features help rangers and "
            "viewers distinguish individual bears without tagging every animal."
        ),
        "before_caption": "Divot watching the current.",
        "card_caption": "Divot during the autumn feeding window.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2022/08/brown-bear-divot-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-divot.jpg",
        "before_key": "b32a-explore",
        "card_key": "b32a-card",
        "seed": 13,
    },
    {
        "id": "b503",
        "name": "Marge",
        "tagline": "A mature female with a strong Brooks River presence.",
        "fact": (
            "Marge is one of many bears whose annual return gives viewers a "
            "chance to compare how different individuals prepare for winter."
        ),
        "before_caption": "Marge along the river’s edge.",
        "card_caption": "Marge in a salmon-rich season.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2022/09/brown-bear-marge-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-marge.jpg",
        "before_key": "b503-explore",
        "card_key": "b503-card",
        "seed": 14,
    },
    {
        "id": "b428",
        "name": "Big Cheeks",
        "tagline": "A large adult bear with a memorable silhouette.",
        "fact": (
            "Late-summer body mass is not merely a contest metric: it is the "
            "energy reserve that supports bears through months of hibernation."
        ),
        "before_caption": "Big Cheeks in the Brooks River.",
        "card_caption": "Big Cheeks in fall condition.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2022/08/brown-bear-big-cheeks-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-big-cheeks.jpg",
        "before_key": "b428-explore",
        "card_key": "b428-card",
        "seed": 15,
    },
    {
        "id": "b144",
        "name": "Venti",
        "tagline": "A large and increasingly familiar Katmai bear.",
        "fact": (
            "Venti’s seasonal transformation illustrates why Fat Bear Week "
            "celebrates successful feeding rather than comparing bears to a "
            "single ideal body shape."
        ),
        "before_caption": "Venti near Brooks Falls.",
        "card_caption": "Venti prepared for winter.",
        "sources": {"before": "explore", "card": "popular_science"},
        "before_url": "https://explore.org/wp-content/uploads/2022/09/brown-bear-venti-katmai.jpg",
        "card_url": "https://www.popsci.com/uploads/2023/10/02/fat-bear-week-venti.jpg",
        "before_key": "b144-explore",
        "card_key": "b144-card",
        "seed": 16,
    },
]

BEARS_BY_ID: dict[str, dict[str, Any]] = {bear["id"]: bear for bear in BEARS}


def get_bear(bear_id: str) -> dict[str, Any] | None:
    """Return a bear record by stable ID, or None if it is not in this roster."""
    if bear_id in BEARS_BY_ID:
        return BEARS_BY_ID[bear_id]
    if not bear_id.startswith("b") and f"b{bear_id}" in BEARS_BY_ID:
        return BEARS_BY_ID[f"b{bear_id}"]
    return None


def media_key_for(bear_id: str, variant: str) -> str | None:
    """
    Return the stable local media key for one bear.

    Valid variants are ``before`` and ``card``. The caller should route the
    returned key through /media/<key>; it should not expose an upstream URL.
    """
    bear = get_bear(bear_id)
    if bear is None:
        return None

    if variant == "before":
        return bear["before_key"]
    if variant == "card":
        return bear["card_key"]
    return None


def public_bear(bear: dict[str, Any]) -> dict[str, Any]:
    """
    Convert an internal roster record into an API-safe payload.

    Source URLs remain server-side so that clients always consume cached local
    media paths and the game remains usable without remote image requests.
    """
    return {
        "id": bear["id"],
        "name": bear["name"],
        "tagline": bear["tagline"],
        "fact": bear["fact"],
        "seed": bear["seed"],
        "media": {
            "before": {
                "key": bear["before_key"],
                "url": f"/media/{bear['before_key']}",
                "caption": bear["before_caption"],
                "source": MEDIA_SOURCES[bear["sources"]["before"]]["label"],
            },
            "card": {
                "key": bear["card_key"],
                "url": f"/media/{bear['card_key']}",
                "caption": bear["card_caption"],
                "source": MEDIA_SOURCES[bear["sources"]["card"]]["label"],
            },
        },
    }


SOURCES: dict[str, str] = {}
for _b in BEARS:
    SOURCES[_b["before_key"]] = _b["before_url"]
    SOURCES[_b["card_key"]] = _b["card_url"]

MATCHES = [
    ('132', '284', 9426, 1598),
    ('806', '901', 6365, 6601),
    ('909', '428', 6367, 6444),
    ('131', '910', 6579, 6202),
    ('694', '620', 5760, 3655),
    ('610', '89', 4851, 8189),
    ('32', '164', 6204, 5496),
    ('151', '903', 3092, 7144),
    ('132', '901', 15689, 9217),
    ('428', '131', 11813, 8132),
    ('694', '89', 4180, 13474),
    ('32', '903', 10123, 7383),
    ('132', '428', 0, 0),
    ('89', '32', 0, 0),
    (None, None, 0, 0),
]

GRID: dict[str, str] = {}
EXTRA: dict[str, tuple[str, str, str]] = {}
for _b in BEARS:
    EXTRA[_b["id"]] = (
        _b["card_url"],
        MEDIA_SOURCES.get(_b["sources"]["card"], {}).get("url", ""),
        _b["card_caption"],
    )
    if _b["id"].startswith("b"):
        EXTRA[_b["id"][1:]] = EXTRA[_b["id"]]

