import './Results.css'

function formatCost(value) {
  const num = Number(value)
  if (num !== num || num < 0) return '—'
  return `₹${Math.round(num).toLocaleString('en-IN')}/year`
}

export default function Results({ data, form, onReset }) {
  const riskClass = (data.risk_category || 'medium').toString().toLowerCase()
  const displayCost = formatCost(data?.estimated_cost)

  return (
    <div className="results">
      <div className="results-card">
        <h1 className="results-title">Your Insurance Estimate</h1>

        <div className="results-cost">
          <span className="cost-label">Estimated Insurance Cost</span>
          <span className="cost-value">{displayCost}</span>
        </div>

        <div className={`results-risk risk-${riskClass}`}>
          <span className="risk-label">Risk Category</span>
          <span className="risk-value">{data.risk_category || '—'}</span>
        </div>

        {data.bmi != null && !Number.isNaN(Number(data.bmi)) && (
          <div className="results-bmi">
            <span>Your BMI: {Number(data.bmi).toFixed(1)}</span>
          </div>
        )}

        <div className="results-suggestions">
          <h3>Suggestions</h3>
          <ul>
            {(Array.isArray(data.suggestions) ? data.suggestions : []).map((s, i) => (
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
