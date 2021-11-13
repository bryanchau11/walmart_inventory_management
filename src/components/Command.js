import { useParams, Link } from 'react-router-dom';

function Command() {
  const { command } = useParams();
  return <div>This is your sql command: {command}</div>;
}
export default Command;
