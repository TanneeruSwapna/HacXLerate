import { Link } from 'react-router-dom';
import '../App.css';

function Dashboard() {
  return (
    <div>
      <h2>Welcome to Qwipo, Retailer!</h2>
      <p>Discover personalized products and optimize your purchases.</p>
      <Link to="/recommendations"><button>Get Recommendations</button></Link>
      <Link to="/catalog"><button>Browse Catalog</button></Link>
      <Link to="/cart"><button>View Cart</button></Link>
    </div>
  );
}

export default Dashboard;