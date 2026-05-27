
import { useState, useEffect } from "react";

function App() {

  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState([]);   // adding of producnt in array 
  const [loading, setLoading] = useState(true);   // for loading status during loading the page
  const [error, setError] = useState("");

 useEffect(() => {

  fetch("https://dummyjson.com/products")   // duummy api hai
    .then((response) => response.json())
    .then((data) => {
      setProducts(data.products);
      setLoading(false);
    })
    .catch(() => {
      setError("Failed to fetch products");
      setLoading(false);
    });


}, []);

console.log(products);
const filteredProducts = products.filter((product) =>   // used for filtered product in show cases
  product.title.toLowerCase().includes(searchText.toLowerCase())  // to be rememebere this line
);
  return (
  <div className="app">

    <h1 className="heading "> Shop Your Product</h1>
    <div className="search-box">
      <input
        type="text"
        placeholder="Search products..."
        value={searchText}
        onChange={(event) => setSearchText(event.target.value)}
      />
      <button> Search</button>
    </div>
    {
       loading &&  <h2> Loading products.......  </h2>
    }

    {
      error && <h2>{error}</h2>
    }

    {
  filteredProducts.length === 0 && !loading && (
    <h2> No products found</h2>
  )
}
    <div className="products-container">

  {
    filteredProducts.map((product) => (

      <div className="product-card" key={product.id}>
        <img
          src={product.thumbnail}
          alt={product.title}
        />

        <h3>{product.title.slice(0,40)}...</h3>  // title range in 0 to 40 bro
        <p>₹ {product.price}</p>
        <p>{product.category}</p>

      </div>

    ))
  }

</div>



  </div>

);
}


export default App;