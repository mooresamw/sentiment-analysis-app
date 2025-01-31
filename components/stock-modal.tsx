"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

// Mock data for the stock price history
const mockPriceHistory = [
  { date: "2023-01-01", price: 150 },
  { date: "2023-02-01", price: 155 },
  { date: "2023-03-01", price: 160 },
  { date: "2023-04-01", price: 158 },
  { date: "2023-05-01", price: 165 },
  { date: "2023-06-01", price: 170 },
]

interface StockModalProps {
  isOpen: boolean
  onClose: () => void
  stock: {
    ticker: string
    companyName: string
    currentPrice: number
    sentiment: number
    confidence: number
    position: string
  }
}

export function StockModal({ isOpen, onClose, stock }: StockModalProps) {
  const [timeRange, setTimeRange] = useState("6M")

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[625px]">
        <DialogHeader>
          <DialogTitle>
            {stock.ticker} - {stock.companyName}
          </DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 items-center gap-4">
            <span className="font-medium">Current Price:</span>
            {/*<span>${stock.currentPrice.toFixed(2)}</span>*/}
            <span className="font-medium">Sentiment Score: {stock.sentiment}</span>
            <span className="font-medium">Confidence Score: {stock.confidence}</span>
            <span className="font-medium">Recommendation: {stock.position}</span>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <h4 className="font-semibold">Price History</h4>
              <Select value={timeRange} onValueChange={setTimeRange}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select time range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1M">1 Month</SelectItem>
                  <SelectItem value="3M">3 Months</SelectItem>
                  <SelectItem value="6M">6 Months</SelectItem>
                  <SelectItem value="1Y">1 Year</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="h-[200px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockPriceHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="price" stroke="#8884d8" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

