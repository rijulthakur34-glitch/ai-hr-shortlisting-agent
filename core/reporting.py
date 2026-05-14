import json
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI Candidate Shortlist</title>
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; background-color: #f9fafb; color: #333; }
    h1 { color: #111827; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #fff; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); }
    th, td { border: 1px solid #e5e7eb; padding: 12px; text-align: left; }
    th { background-color: #f3f4f6; font-weight: 600; color: #374151; }
    .score { font-size: 1.1em; font-weight: bold; }
    .justification { display: block; font-size: 0.85em; color: #6b7280; margin-top: 4px; }
    .hire { color: #059669; font-weight: bold; }
    .no-hire { color: #dc2626; font-weight: bold; }
</style>
</head>
<body>
    <h1>AI Candidate Shortlist Report</h1>
    <table>
        <tr>
            <th>Candidate Details</th>
            <th>Dimension Scores</th>
            <th>Areas of Concern & Questions</th>
            <th>Recommendation</th>
        </tr>
        {% for c in candidates %}
        <tr>
            <td>
                <strong>{{ c.name }}</strong><br>
                <span class="score" style="font-size: 1.5em; color: #7c3aed;">{{ c.total_score }} / 10</span>
            </td>
            <td>
                <div style="margin-bottom: 10px;">
                    <strong>Skills:</strong> {{ c.skills_match.score }}
                    <span class="justification">{{ c.skills_match.justification }}</span>
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Exp:</strong> {{ c.experience_relevance.score }}
                    <span class="justification">{{ c.experience_relevance.justification }}</span>
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Proj:</strong> {{ c.project_portfolio.score }}
                    <span class="justification">{{ c.project_portfolio.justification }}</span>
                </div>
            </td>
            <td>
                <div style="margin-bottom: 10px;">
                    <strong>🚩 Gaps:</strong> {{ c.experience_gaps }}<br>
                    <strong>Missing Skills:</strong> {{ c.missing_skills | join(', ') if c.missing_skills else 'None' }}
                </div>
                <div>
                    <strong>❓ Interview Questions:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; font-size: 0.9em;">
                    {% for q in c.suggested_questions %}
                        <li>{{ q }}</li>
                    {% endfor %}
                    </ul>
                </div>
            </td>
            <td class="{{ 'hire' if c.recommendation == 'Hire' else 'no-hire' }}" style="text-align: center;">
                {{ c.recommendation }}
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def generate_html_report_str(results: list) -> str:
    template = Template(HTML_TEMPLATE)
    return template.render(candidates=results)
