function Section({ title, children }) {
  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <h3 className="text-lg font-semibold text-gray-100 mb-3">{title}</h3>
      {children}
    </div>
  );
}

function severityColor(severity) {
  if (severity === "critical") return "text-red-400";
  if (severity === "warning") return "text-yellow-400";
  return "text-gray-400";
}

export default function ResultsView({ result }) {
  return (
    <div className="w-full max-w-4xl mx-auto mt-8 space-y-6">
      <Section title="Development Plan">
        <pre className="whitespace-pre-wrap text-sm text-gray-300">{result.plan}</pre>
      </Section>

      <Section title={`Generated Files (${result.generated_files.length})`}>
        <ul className="text-sm text-gray-300 space-y-1 list-disc list-inside">
          {result.generated_files.map((path) => (
            <li key={path}>{path.split(/[\\/]/).pop()}</li>
          ))}
        </ul>
      </Section>

      <Section title={`Review Report (${result.review_report.length} issues)`}>
        {result.review_report.length === 0 ? (
          <p className="text-sm text-gray-400">No issues found.</p>
        ) : (
          <ul className="text-sm space-y-2">
            {result.review_report.map((issue, i) => (
              <li key={i}>
                <span className={`font-semibold ${severityColor(issue.severity)}`}>
                  [{issue.severity}]
                </span>{" "}
                <span className="text-gray-300">{issue.file}:</span>{" "}
                <span className="text-gray-400">{issue.description}</span>
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="README.md">
        <pre className="whitespace-pre-wrap text-sm text-gray-300 max-h-96 overflow-y-auto">
          {result.readme_content}
        </pre>
      </Section>

      <Section title="Commit Message">
        <code className="text-sm text-green-400">{result.commit_message}</code>
      </Section>
    </div>
  );
}