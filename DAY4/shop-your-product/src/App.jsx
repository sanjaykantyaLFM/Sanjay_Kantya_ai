import { useState, useEffect } from "react";


function App(){

  // useState use here
  const [searchText, setSearchText] = useState("");   // initialy we have empty value in useState
                                                    // initialy search text is "" empty

  const [products, setProducts] = useState([]);  // initialy here we store products [] 
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");



  useEffect( () => {

    fetch(" https://fakestoreapi.com/products")

      .then((response) => response.json())

      .then((data) => {
        setProducts(data);
        setLoading(false);
      })

      .catch(() => {
        setError("failed to get product")
        setLoading(false);
      })
  }, []);

  console.log(products);



  {
    loading && <h2>Loading products...</h2>  
  }
  {
    error && <h2>{error}</h2>
  }
//  this is used for filtered the products
  const filteredProducts = products.filter((product) =>  
    product.title.toLowerCase().includes(searchText.toLowerCase())
  );


  return (
    <div>
      <h1> Shop Your Product</h1>
      {/* <input type = "text" placeholder="Search your product here"/> */}
      {/* <input type="text" />   thiis is normal uncontrolled input value here browser internally store value */}
      <input 
        type="text"
        placeholder="Search products"
        value = {searchText}  // input value is controled by react using value
        onChange = {(event) => setSearchText(event.target.value)}    // onChange means whenever user type and  event contains input event information  
      />                                                        {/* event.target.value means current input valuE */}

      
      <button>Search</button>
      <h2>{searchText }</h2>

      {/* Adding product using api */} {/*  map is used to display all prodycts in array*/}
      {
        filteredProducts.map((product) => (   
          <div key = {product.id}>

            <img
              src= {product.image}
              alt = {product.title}
              width = "150"
            />

            <h3>{product.title}</h3>
            <h3>{product.price}</h3>
            <h3>{product.category}</h3>

          </div>
        ))
      }

    </div>

  )
}

export default App;