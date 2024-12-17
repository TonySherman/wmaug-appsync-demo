'use client';

import { useState, useEffect } from 'react';

import appsyncClient from "../graphql/config";
import { Products } from "@/graphql/queries";
import { Product } from '@/types/graphql'
import { useRouter } from 'next/navigation';



const client = appsyncClient;

export default function Home() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [nextToken, setNextToken] = useState<string | null | undefined>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchProducts = async (token?: string | null) => {
    try {
      const { data } = await client.graphql({
        query: Products,
        variables: {
          limit: 10,
          nextToken: token
        }
      });

      const newProducts = data.Products?.items?.filter((product): product is Product => product != null) || [];
      
      setProducts(prev => token ? [...prev, ...newProducts] : newProducts);
      
      // Update nextToken
      setNextToken(data.Products?.nextToken);
      setLoading(false);
    } catch (err) {
      console.error('Error loading products:', err);
      setError(err instanceof Error ? err : new Error('Unknown error'));
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleLoadMore = () => {
    if (nextToken) {
      fetchProducts(nextToken);
    }
  };

  const handleProductClick = (sku: string) => {
    router.push(`/product/${sku}`);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading products: {error.message}</div>;

  return (
    <div className="flex flex-col items-center m-2">
        <h1 className="text-3xl font-bold m-5">
          Products
        </h1>
        <table className="border-collapse border border-slate-500 w-full cursor-pointer">
          <thead>
            <tr>
              <th className="border border-slate-600 p-2">SKU</th>
              <th className="border border-slate-600 p-2">Name</th>
              <th className="border border-slate-600 p-2">Description</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr 
                className="hover:bg-sky-700" 
                key={product.sku ?? 'unknown'}
                onClick={() => handleProductClick(product.sku ?? "unknown")}
              >
                <td className="border border-slate-700 p-2">{product.sku}</td>
                <td className="border border-slate-700 p-2">{product.name}</td>
                <td className="border border-slate-700 p-2">{product.description}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {nextToken && (
          <button 
            onClick={handleLoadMore}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Load More
          </button>
        )}
    </div>
  );
}
