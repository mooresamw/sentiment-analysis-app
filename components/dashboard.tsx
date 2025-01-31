"use client"

import {useEffect, useState} from "react"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {StockModal} from "@/components/stock-modal";

export function Dashboard() {
  const [searchTerm, setSearchTerm] = useState("")
  const [stockData, setStockData] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedStock, setSelectedStock] = useState(null)

  // Grab sentiment analysis data from backend api on page load, then on interval
  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await fetch("http://localhost:8080/api/", {/*mode: 'no-cors' } */})
        const data = await response.json()
        setStockData(data)
        setIsLoading(false)
        console.log("Fetched")
      } catch (error) {
        console.log("Error fetching data: ", error)
      }
    }

    // Interval for fetching backend api
    fetchStockData()
    const interval = setInterval(fetchStockData, 30000) // Fetch every 30 seconds
  }, []);
  if (isLoading) {
    return ("Page Loading")
  } else {
    let filteredStocks = stockData.filter((stock) => stock.ticker.toLowerCase().includes(searchTerm.toLowerCase()))
    return (
        <div className="container mx-auto py-10">
          <Card>
            <CardHeader>
              <CardTitle>Sentiment Analysis Dashboard</CardTitle>
              <CardDescription>
                View sentiment analysis, confidence scores, and position recommendations for various stocks.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <Input
                    placeholder="Search stocks..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="max-w-sm"
                />
              </div>
              <Table>
                <TableCaption>Live Sentiment Analysis Beta</TableCaption>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ticker</TableHead>
                    <TableHead>Sentiment Score</TableHead>
                    <TableHead>Confidence Score</TableHead>
                    <TableHead>Recommendation</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredStocks.map((stock) => (
                      <TableRow className="hover:bg-muted/50" key={stock.ticker}>
                        <TableCell className="font-medium cursor-pointer hover:font-bold" onClick={() => setSelectedStock(stock)}>{stock.ticker}</TableCell>
                        <TableCell>{stock.sentiment}</TableCell>
                        <TableCell>{stock.confidence}</TableCell>
                        <TableCell className={
                                      stock.position === 'buy' ? 'text-green-500' :
                                      stock.position === 'sell' ? 'text-red-500' :
                                      stock.position === 'hold' ? 'text-yellow-500' :
                                      '' }>
                          {stock.position}
                        </TableCell>
                      </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          {selectedStock && (
        <StockModal isOpen={!!selectedStock} onClose={() => setSelectedStock(null)} stock={selectedStock} />
          )}
    </div>
    )
  }
}