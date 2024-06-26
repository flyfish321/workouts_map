import YearStat from '@/components/YearStat';
import {
  CHINESE_LOCATION_INFO_MESSAGE_FIRST,
  CHINESE_LOCATION_INFO_MESSAGE_SECOND,
} from '@/utils/const';
import CitiesStat from './CitiesStat';
import LocationSummary from './LocationSummary';
import PeriodStat from './PeriodStat';

interface ILocationStatProps {
  changeYear: (_year: string) => void;
  changeCity: (_city: string) => void;
  changeType: (_type: string) => void;
  onClickTypeInYear: (_year: string, _type: string) => void;
}

const LocationStat = ({ changeYear, changeCity, changeType, onClickTypeInYear }: ILocationStatProps) => (
  <div className="fl w-100-l pb5 pr5-l">
    <section className="pb4" style={{ paddingBottom: '0rem' }}>
       <p style={{ lineHeight: 1.8 }}>
        {CHINESE_LOCATION_INFO_MESSAGE_FIRST}
        <br />
        <br />
        {CHINESE_LOCATION_INFO_MESSAGE_SECOND}
        <br />
        The best is yet to come.
      </p>
    </section>
    <hr color="red" />
    <LocationSummary />
    <CitiesStat onClick={changeCity} />
    <PeriodStat onClick={changeType} />
    <YearStat year="Total" onClick={changeYear} onClickTypeInYear={onClickTypeInYear}/>
  </div>
);

export default LocationStat;
