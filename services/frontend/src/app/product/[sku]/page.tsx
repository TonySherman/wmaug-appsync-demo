'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Product, ProductCount } from '@/types/graphql';
import appsyncClient from '@/graphql/config';

const client = appsyncClient;

type productReview = {
  author: string
  rating: number
  review: string
}

export default function ProductDetailPage() {
  const params = useParams<{ sku: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [count, setCount] = useState< ProductCount | null>(null);
  const [reviews, setReviews] = useState< productReview[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchProductDetails() {
      try {
        const res = await client.graphql({
	query: `query MyQuery($sku: String = "", $sku: String = "") {
		  Product(sku: $sku) {
		    name
		    description
		}
		  getInventory(sku: $sku) {
		    available_count
		}
		  getProductReviews(sku: $sku) {
		    author
		    rating
		    review
                 }
	      }`,
          variables: {
            sku: params.sku
          }
        });

	if (res && 'data' in res) {
	  const data = res.data;
	  setProduct(data.Product);
	  setCount(data.getInventory);
	  setReviews(data.getProductReviews);
	  setLoading(false);
	}

      } catch (err) {
        console.error('Error loading product details:', err);
        setError(err instanceof Error ? err : new Error('Unknown error'));
        setLoading(false);
      }
    }

    if (params.sku) {
      fetchProductDetails();
    }
  }, [params.sku]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading product: {error.message}</div>;
  if (!product) return <div>Product not found</div>;

  return (
    <div className="flex flex-col items-center">
      <h1 className="text-5xl font-bold text-center m-5">{product.name}</h1>
      <div className="gap-4 text-2xl content-center m-5">
        <div>
          <p><strong>SKU:</strong> {params.sku}</p>
          <p><strong>Description:</strong> {product.description}</p>
          <p><strong>Quantity:</strong> {count?.available_count}</p>
        </div>
      </div>

      {reviews && (<table className="border-collapse border border-slate-500 m-5 table-auto">
	<thead>
	  <tr>
	    <th className="border border-slate-600 p-2">Rating</th>
	    <th className="border border-slate-600 p-2">Author</th>
	    <th className="border border-slate-600 p-2">Review</th>
	  </tr>
	</thead>
	  <tbody>
	    {reviews.map((review, index) => (
	      <tr key={`${index}-${review.author}-${review.rating}`}>
		<td className="border border-slate-700 p-2">
		  {Array(review.rating)
		    .fill(0)
		    .map((_, starIndex) => (
		      <span key={starIndex} className="text-yellow-400">★</span>
		    ))}
		</td>
		<td className="border border-slate-700 p-2">{review.author}</td>
		<td className="border border-slate-700 p-2">{review.review}</td>
	      </tr>
	    ))}
	  </tbody>
      </table>)}
    </div>
  );
}
