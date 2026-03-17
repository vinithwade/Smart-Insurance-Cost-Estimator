export default function StepFinancial({
  form,
  updateForm,
  prevStep,
  submitForm,
  isLast,
  loading,
  error,
}) {
  return (
    <>
      <h2 className="step-title">Financial Information</h2>
      <div className="form-group">
        <label>Annual Income (₹)</label>
        <input
          type="number"
          min="0"
          placeholder="800000"
          value={form.income}
          onChange={(e) => updateForm({ income: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Savings (₹)</label>
        <input
          type="number"
          min="0"
          placeholder="200000"
          value={form.savings}
          onChange={(e) => updateForm({ savings: e.target.value })}
        />
      </div>
      {error && <div className="form-error">{error}</div>}
      <div className="form-actions">
        <button className="btn btn-secondary" onClick={prevStep} disabled={loading}>
          Back
        </button>
        <button
          className="btn btn-primary"
          onClick={submitForm}
          disabled={loading}
        >
          {loading ? 'Calculating...' : 'Get Estimate'}
        </button>
      </div>
    </>
  )
}
