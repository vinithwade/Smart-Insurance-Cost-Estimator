export default function StepHealth({ form, updateForm, nextStep, prevStep }) {
  return (
    <>
      <h2 className="step-title">Health Conditions</h2>
      <div className="form-group">
        <label>Do you have diabetes?</label>
        <select
          value={form.diabetes}
          onChange={(e) => updateForm({ diabetes: e.target.value })}
        >
          <option value="no">No</option>
          <option value="yes">Yes</option>
        </select>
      </div>
      <div className="form-group">
        <label>Do you have heart problems?</label>
        <select
          value={form.heartProblems}
          onChange={(e) => updateForm({ heartProblems: e.target.value })}
        >
          <option value="no">No</option>
          <option value="yes">Yes</option>
        </select>
      </div>
      <div className="form-group">
        <label>Any chronic disease?</label>
        <select
          value={form.chronicDisease}
          onChange={(e) => updateForm({ chronicDisease: e.target.value })}
        >
          <option value="no">No</option>
          <option value="yes">Yes</option>
        </select>
      </div>
      <div className="form-actions">
        <button className="btn btn-secondary" onClick={prevStep}>
          Back
        </button>
        <button className="btn btn-primary" onClick={nextStep}>
          Next
        </button>
      </div>
    </>
  )
}
