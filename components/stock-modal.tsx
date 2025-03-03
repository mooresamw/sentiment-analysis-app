"use client"

import {useState} from "react"
import {Dialog, DialogContent, DialogHeader, DialogTitle} from "@/components/ui/dialog"
import {CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts"
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";

export function StockModal({ isOpen, onClose, stock, prices, currentPrice, company, recentNews}: any) {

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[625px]">
        <DialogHeader>
          <DialogTitle>
            {stock.ticker} - {company}
          </DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 items-center gap-4">
            <span className="font-medium">Current Price: ${currentPrice}</span>
            <span className="font-medium">Sentiment Score: {stock.sentiment}</span>
            <span className="font-medium">Confidence Score: {stock.confidence}</span>
            <span className="font-medium">Recommendation: {stock.position}</span>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <h4 className="font-semibold">Live Prices</h4>
              {/*<Select value={timeRange} onValueChange={setTimeRange}>*/}
              {/*  <SelectTrigger className="w-[180px]">*/}
              {/*    <SelectValue placeholder="Select time range" />*/}
              {/*  </SelectTrigger>*/}
              {/*  <SelectContent>*/}
              {/*    <SelectItem value="1M">1 Month</SelectItem>*/}
              {/*    <SelectItem value="3M">3 Months</SelectItem>*/}
              {/*    <SelectItem value="6M">6 Months</SelectItem>*/}
              {/*    <SelectItem value="1Y">1 Year</SelectItem>*/}
              {/*  </SelectContent>*/}
              {/*</Select>*/}
            </div>
            <div className="h-[200px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={prices}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={false} />
                  <YAxis domain={[Math.min(...prices.map((d: { price: any }) => d.price)) - 1, Math.max(...prices.map((d: { price: any }) => d.price)) + 1]} />
                  <Tooltip isAnimationActive={true} />
                  <Line type='linear' dataKey="price" stroke="#063970" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          <Card>
            <CardHeader>
              <CardTitle>Recent News</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {recentNews.map((article: any, index: any) => {
                  // Format timestamp to a readable date
                  const formattedDate = new Date(article.timestamp).toLocaleString();

                  // Extract tickers (convert comma-separated string into an array)
                  const tickers = article.ticker.split(",");

                  // Get prices for each ticker and format them
                  const priceList = tickers
                    .map((ticker: string) => {
                      const price = article.prices_at_date?.[ticker]; // Get price if exists
                      return price ? `${ticker}: $${price.toFixed(2)}` : null;
                    })
                    .filter(Boolean) // Remove null values

                  // Determine the relevant ticker dynamically (assuming it's the first ticker in the list)
                  const selectedTicker = tickers.find((t: string) => stock.ticker === t);

                  // Get price for the specific ticker
                  const price = selectedTicker ? article.prices_at_date[selectedTicker] : null;
                  const formattedPrice = price !== null ? `$${price.toFixed(2)}` : "N/A";

                  return (
                    <li key={index} className="text-sm">
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        {article.title}
                      </a>
                      <p className="text-gray-600">
                        Date: {formattedDate} | Price at release: {priceList.length > 0 ? formattedPrice : "N/A"}
                      </p>
                    </li>
                  );
                })}
              </ul>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  )
}

