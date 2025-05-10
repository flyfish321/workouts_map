import Stat from '@/components/Stat';
import useActivities from '@/hooks/useActivities';

// only support China for now
const LocationSummary = () => {
  const { years, countries, provinces, cities } = useActivities();
  return (
    <div className="cursor-pointer">
      <section>
        {years ? <Stat value={`${years.length}`} description=" 年里我走过" /> : null}
        {countries ? <Stat value={countries.length} description="/195 个国家" /> : null}
        {provinces ? <Stat value={provinces.length} description="/34 个中国省级行政区" /> : null}
        {cities ? (
          <Stat value={Object.keys(cities).length} description="/333 个中国地级行政区" />
        ) : null}
      </section>
      <hr color="red" />
    </div>
  );
};

export default LocationSummary;
