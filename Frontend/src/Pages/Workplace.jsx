import { teamMembers } from "../data/sampleData";

export default function Workplace() {
  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            People & operations
          </span>

          <h2>Workplace</h2>

          <p>
            Manage team roles, shifts and
            availability.
          </p>
        </div>
      </div>

      <section className="panel">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Team Member</th>
                <th>Role</th>
                <th>Contact</th>
                <th>Shift</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {teamMembers.map((member) => (
                <tr key={member.id}>
                  <td>
                    <strong>{member.name}</strong>
                  </td>

                  <td>{member.role}</td>
                  <td>{member.phone}</td>
                  <td>{member.shift}</td>

                  <td>
                    <span
                      className={`status ${
                        member.status === "Active"
                          ? "completed"
                          : "pending"
                      }`}
                    >
                      {member.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}