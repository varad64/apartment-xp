import { useEffect, useState } from "react";
import { getFlats, getTotalArea, submitBills } from "./api.js";
import "./App.css";

const CATEGORIES = [
  { key: "security", label: "Security deposit" },
  { key: "electricity", label: "Common electricity" },
  { key: "water", label: "Common water" },
];

const emptyBills = () =>
  Object.fromEntries(CATEGORIES.map(({ key }) => [key, { amount: "", file: null }]));

export default function App() {
  const [flats, setFlats] = useState([]);
  const [totalArea, setTotalArea] = useState(null);
  const [loadError, setLoadError] = useState("");

  const [bills, setBills] = useState(emptyBills);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    Promise.all([getFlats(), getTotalArea()])
      .then(([flatList, area]) => {
        setFlats(flatList);
        setTotalArea(area);
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  const updateBill = (key, changes) =>
    setBills((prev) => ({ ...prev, [key]: { ...prev[key], ...changes } }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitError("");
    setResult(null);

    // Send a manual amount when given, otherwise the image. The backend rejects a category with neither.
    const payload = {};
    for (const { key } of CATEGORIES) {
      const { amount, file } = bills[key];
      if (amount) {
        payload[key] = { amount };
      } else if (file) {
        payload[key] = { file };
      }
    }

    setSubmitting(true);
    try {
      setResult(await submitBills(payload));
    } catch (err) {
      setSubmitError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="container">
      <h1>Apartment Society</h1>

      {loadError && <p className="error">Could not reach the backend: {loadError}</p>}

      <section className="card">
        <h2>Flats</h2>
        <p>
          Total chargeable area: <strong>{totalArea ?? "–"}</strong> sq ft
        </p>
        <table>
          <thead>
            <tr>
              <th>Flat</th>
              <th>Family</th>
              <th>Area</th>
              <th>Servant room</th>
              <th>Chargeable area</th>
            </tr>
          </thead>
          <tbody>
            {flats.map((flat) => (
              <tr key={flat.flat_number}>
                <td>{flat.flat_number}</td>
                <td>{flat.family_name}</td>
                <td>{flat.area}</td>
                <td>{flat.servant_room ? flat.servant_room.room_number : "–"}</td>
                <td>{flat.area + (flat.servant_room?.area ?? 0)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="card">
        <h2>Submit bills</h2>
        <p className="hint">
          For each category, enter the amount <em>or</em> upload a JPEG bill for OCR extraction.
        </p>
        <form onSubmit={handleSubmit}>
          {CATEGORIES.map(({ key, label }) => (
            <fieldset key={key}>
              <legend>{label}</legend>
              <label>
                Amount (₹)
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={bills[key].amount}
                  onChange={(e) => updateBill(key, { amount: e.target.value })}
                  placeholder="e.g. 31152.00"
                />
              </label>
              <label>
                Bill image (JPEG)
                <input
                  type="file"
                  accept="image/jpeg"
                  onChange={(e) => updateBill(key, { file: e.target.files[0] ?? null })}
                />
              </label>
            </fieldset>
          ))}
          <button type="submit" disabled={submitting}>
            {submitting ? "Submitting…" : "Calculate shares"}
          </button>
        </form>

        {submitError && <p className="error">{submitError}</p>}

        {result && <Result result={result} />}
      </section>
    </main>
  );
}

function Result({ result }) {
  return (
    <div className="result">
      <h3>Result</h3>
      <p>
        Total to split: <strong>{result.total_amount}</strong>
      </p>

      <h4>Line items</h4>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Amount</th>
            <th>Source</th>
          </tr>
        </thead>
        <tbody>
          {result.line_items.map((item, i) => (
            <tr key={i}>
              <td>{item.category}</td>
              <td>{item.amount}</td>
              <td>{item.source}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h4>Shares per flat</h4>
      <table>
        <thead>
          <tr>
            <th>Flat</th>
            <th>Area</th>
            <th>Share</th>
          </tr>
        </thead>
        <tbody>
          {result.shares.map((share) => (
            <tr key={share.flat_number}>
              <td>{share.flat_number}</td>
              <td>{share.area}</td>
              <td>{share.share_amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
