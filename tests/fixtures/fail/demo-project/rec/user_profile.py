from collections import Counter


def build_user_profile(events):
    """根据会员最近的行为事件统计偏好分类。"""
    counts = Counter(e["category"] for e in events)
    return {"top_categories": [category for category, _ in counts.most_common(3)]}


def recommend(member_id, events):
    """基于会员偏好分类返回推荐结果。"""
    profile = build_user_profile(events)
    return {
        "member_id": member_id,
        "suggestions": profile["top_categories"],
    }
