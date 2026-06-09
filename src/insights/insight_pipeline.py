
from .insights_generator import generate_insights
from .generate_story import generate_story


def insight_pipeline(report):

    insights = generate_insights(report)

    story = generate_story(insights)

    return {
            'report' : report,
            'insights': insights,
            'story' : story
            }