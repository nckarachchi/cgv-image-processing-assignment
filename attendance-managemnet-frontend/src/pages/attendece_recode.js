import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [studentIndex, setStudentIndex] = useState('');
  const [attendanceSummary, setAttendanceSummary] = useState(null);

  const fetchAttendanceSummary = async () => {
    try {
      const response = await axios.get(`/attendance_summary?index=${studentIndex}`);
      setAttendanceSummary(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Student Attendance Summary</h1>
      <input
        type="text"
        placeholder="Enter Student Index"
        value={studentIndex}
        onChange={(e) => setStudentIndex(e.target.value)}
      />
      <button onClick={fetchAttendanceSummary}>Fetch Summary</button>
      {attendanceSummary && (
        <div>
          <p>Total Entries: {attendanceSummary.total_entries}</p>
          <p>Present Count: {attendanceSummary.present_count}</p>
          <p>Absent Count: {attendanceSummary.absent_count}</p>
          <img
            src={`data:image/png;base64,${attendanceSummary.attendance_chart}`}
            alt="Attendance Chart"
          />
        </div>
      )}
    </div>
  );
}

export default App;
