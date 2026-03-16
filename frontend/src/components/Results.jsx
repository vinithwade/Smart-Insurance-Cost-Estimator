import './Results.css'

export default function Results({ data, form, onReset }) {
  const riskClass = data.risk_category?.toLowerCase() || 'medium'

  return (
    <div className="results">
      <div className="results-card">
        <h1 className="results-title">Your Insurance Estimate</h1>

        <div className="results-cost">
          <span className="cost-label">Estimated Insurance Cost</span>
          <span className="cost-value">
            ₹{data.estimated_cost?.toLocaleString('en-IN')}/year
          </span>
        </div>

        <div className={`results-risk risk-${riskClass}`}>
          <span className="risk-label">Risk Category</span>
          <span className="risk-value">{data.risk_category}</span>
        </div>

        {data.bmi && (
          <div className="results-bmi">
            <span>Your BMI: {data.bmi}</span>
          </div>
        )}

        <div className="results-suggestions">
          <h3>Suggestions</h3>
          <ul>
            {data.suggestions?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>

        <button className="btn btn-primary results-reset" onClick={onReset}>
          Start New Assessment
        </button>
      </div>
    </div>
  )
}
