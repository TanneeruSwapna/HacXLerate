import { useNavigate } from 'react-router-dom';
import AddProduct from '../components/AddProduct';
import './AddProductPage.css';

function AddProductPage() {
    const navigate = useNavigate();

    const handleProductAdded = (product) => {
        // Optionally redirect to catalog or show success message
        console.log('Product added:', product);
        navigate('/products');
    };

    const handleCancel = () => {
        navigate('/products');
    };

    return (
        <div className="add-product-page">
            <AddProduct
                onProductAdded={handleProductAdded}
                onCancel={handleCancel}
            />
        </div>
    );
}

export default AddProductPage;
