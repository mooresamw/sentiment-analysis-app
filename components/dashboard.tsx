"use client"

import {useEffect, useState} from "react"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import {ArrowUpDown, Filter} from "lucide-react"
import {StockModal} from "@/components/stock-modal";
import Loading from "@/components/loading"

export function Dashboard() {

  // state variables
  const [searchTerm, setSearchTerm] = useState("")
  const [stockData, setStockData] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedStock, setSelectedStock] = useState(null)
  const [stockPrices, setStockPrices] = useState([])
  const [companyName , setCompanyName] = useState("")
  const [lastPrice, setLastPrice] = useState(0)
  const [sortOrder, setSortOrder] = useState("default")
  const [recentNews, setRecentNews] = useState([])
  const [priceChangeThreshold, setPriceChangeThreshold] = useState("")

  // Grab sentiment analysis data from backend api on page load, then on interval
  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await fetch("http://localhost:8080/api/", {/*mode: 'no-cors' } */})
        const data = await response.json()
        setStockData(data)
        setIsLoading(false)
        console.log("Fetched")
        console.log(data)
      } catch (error) {
        console.log("Error fetching data: ", error)
      }
    }

    // Interval for fetching backend api
    fetchStockData()
    //const interval = setInterval(fetchStockData, 30000) // Fetch every 30 seconds
  }, []);

  const fetchPrices = async (ticker: string) => {
    try {
        const response = await fetch(`http://localhost:8080/api/ticker/${ticker}/get_period_data`, {/*mode: 'no-cors' } */})
        const data = await response.json()
        setStockPrices(data)
        console.log("Fetched")
      } catch (error) {
      console.log("Error fetching data: ", error)
    }
  }

  // Function to send a request to the api to gather current price of a stock
  const fetchCompanyData = async (ticker: string) => {
    try {
        const response = await fetch(`http://localhost:8080/api/ticker/${ticker}/get_current_price`, {/*mode: 'no-cors' } */})
        const data = await response.json()
        setLastPrice(data.current_price)
        setCompanyName(data.company_name)
      } catch (error) {
      console.log("Error fetching data: ", error)
    }
  }

  const fetchRecentNews = async (ticker: string) => {
    try {
      const response = await fetch(`http://localhost:8080/api/ticker/${ticker}/get_recent_news`, {})
      const data = await response.json()
      setRecentNews(data)

    } catch (error) {
      console.log("Error fetching data: ", error)
    }
  }

  if (isLoading) {
    return (<Loading />);
  } else {
    const filteredStocks = stockData
      .filter((stock) => stock.ticker.toLowerCase().includes(searchTerm.toLowerCase()))
      .filter((stock) => {
        if (priceChangeThreshold === "") return true
        const threshold = Number.parseFloat(priceChangeThreshold)
        const priceChange = Number.parseFloat(stock.price_change)
        return threshold >= 0 ? priceChange >= threshold : priceChange <= threshold
      })
      .sort((a, b) => {
        if (sortOrder === "default") return 0
        return sortOrder === "desc" ? b.sentiment - a.sentiment : a.sentiment - b.sentiment
      })
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
                <Input
                  type="number"
                  placeholder="Price change threshold..."
                  value={priceChangeThreshold}
                  onChange={(e) => setPriceChangeThreshold(e.target.value)}
                  className="max-w-sm"
                />
                <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline">
                    <ArrowUpDown className="mr-2 h-4 w-4" />
                    Sort Sentiment
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem onClick={() => setSortOrder("default")}>Default Order</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSortOrder("desc")}>Highest First</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSortOrder("asc")}>Lowest First</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              </div>
              <Table>
                <TableCaption>Live Sentiment Analysis Beta</TableCaption>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ticker</TableHead>
                    <TableHead>Sentiment Score</TableHead>
                    <TableHead>Confidence Score</TableHead>
                    <TableHead>Price Change (%) From Most Recent News</TableHead>
                    <TableHead>Recommendation</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredStocks.map((stock) => (
                      <TableRow className="hover:bg-muted/50" key={stock.ticker}>
                        <TableCell className="font-medium cursor-pointer hover:font-bold" onClick={() =>
                        {setSelectedStock(stock); fetchPrices(stock.ticker); fetchCompanyData(stock.ticker);
                        fetchRecentNews(stock.ticker);}}
                        >{stock.ticker}</TableCell>
                        <TableCell>{stock.sentiment}</TableCell>
                        <TableCell>{stock.confidence}</TableCell>
                        <TableCell>{stock.price_change}</TableCell>
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
        <StockModal isOpen={!!selectedStock} onClose={() => setSelectedStock(null)} stock={selectedStock}
                    prices={stockPrices} currentPrice={lastPrice} company={companyName} recentNews={recentNews} />
          )}
    </div>
    )
  }
}