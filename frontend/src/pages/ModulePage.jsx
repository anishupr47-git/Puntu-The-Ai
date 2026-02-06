import Card from '../components/ui/Card'

export default function ModulePage({ title, tagline, insights }) {
  return (
    <div className="space-y-6">
      <div>
        <div className="text-3xl font-semibold">{title}</div>
        <div className="text-mist">{tagline}</div>
      </div>
      <div className="grid gap-6 md:grid-cols-3">
        {insights.map((item) => (
          <Card key={item.title}>
            <div className="text-sm uppercase tracking-wide text-mist">{item.kicker}</div>
            <div className="mt-2 text-lg font-semibold">{item.title}</div>
            <div className="mt-2 text-sm text-glacier">{item.body}</div>
          </Card>
        ))}
      </div>
    </div>
  )
}
