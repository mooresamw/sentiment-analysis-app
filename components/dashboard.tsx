"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

// Mock data for demonstration
const mockStockData = [
  { ticker: "AAPL", sentiment: 0.8, confidence: 0.9, recommendation: "Buy" },
  { ticker: "GOOGL", sentiment: 0.6, confidence: 0.75, recommendation: "Hold" },
  { ticker: "MSFT", sentiment: 0.7, confidence: 0.85, recommendation: "Buy" },
  { ticker: "AMZN", sentiment: 0.5, confidence: 0.6, recommendation: "Hold" },
  { ticker: "TSLA", sentiment: 0.4, confidence: 0.5, recommendation: "Sell" },
]

export function Dashboard() {
  const [searchTerm, setSearchTerm] = useState("")

  const filteredStocks = mockStockData.filter((stock) => stock.ticker.toLowerCase().includes(searchTerm.toLowerCase()))

  return (
    <div className="container mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle>Stock Sentiment Analysis Dashboard</CardTitle>
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
            <TableCaption>Stock Sentiment Analysis Results</TableCaption>
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
                <TableRow key={stock.ticker}>
                  <TableCell className="font-medium">{stock.ticker}</TableCell>
                  <TableCell>{stock.sentiment.toFixed(2)}</TableCell>
                  <TableCell>{stock.confidence.toFixed(2)}</TableCell>
                  <TableCell>{stock.recommendation}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}