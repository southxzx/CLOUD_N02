import React from 'react';
import {
  StyleSheet,
  Button,
  View,
  ImageBackground,
  Text,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  StatusBar,
} from 'react-native';

// Utils
import { getLocationId, getWeather, getCurrentTemp,getNextTemp } from './utils/api';
import getImageForWeather from './utils/getImageForWeather';
import getIconForWeather from './utils/getIconForWeather';

// Search component
import SearchInput from './SearchInput';

// MomentJS
//import moment from 'moment';
// CLASS
export default class App extends React.Component {
  constructor(props) {
    super(props);
    // bind SCOPE
    this.handleDate = this.handleDate.bind(this);

    // STATE
    this.state = {
      loading: false,
      error: false,
      location: '',
      temperature: 0,
      weather: '',
      created: '2000-01-01T00:00:00.000000Z',
      currentTemp:'',
      currentHumid:'',
      nextTemp:'',
      inputTemp:'0',
      inputHumid: '0'
    };

  }
  // Life cycle
  componentDidMount() {
    this.handleUpdateLocation('Kiev');
  }

  // Parse of date
  handleDate = () => {};

  // Update current location
  handleUpdateLocation = async Temp => {
    if (!Temp) return;

    this.setState({ loading: true }, async () => {
      try {
        const ID = await getLocationId('Kiev');
        const { location, weather, temperature, created } = await getWeather(ID);
        const {currentHumid,currentTemp} = await getCurrentTemp();
        const {nextTemp} = await getNextTemp(this.state["inputTemp"],this.state["inputHumid"]);    
        console.log(nextTemp);
        this.setState({
          loading: false,
          error: false,
          location,
          weather,
          temperature,
          created,
          currentTemp,
          currentHumid,
          nextTemp
        });
      } catch (e) {

        this.setState({
          loading: false,
          error: true,
          currentTemp: 0,
          currentHumid:0
        });

      }
    });
  };

  // inputTempUpdate = text => {
  //   this.setState({
  //     inputTemp: text
  //   });
  // };

  // inputHumidUpdate = text =>{
  //   this.setState({
  //     inputHumid: text
  //   });
  // };
  // RENDERING
  render() {

    // GET values of state
    const { loading, error, location, weather, temperature, created, currentTemp, currentHumid, nextTemp} = this.state;
    // Activity
    return (
      <KeyboardAvoidingView style={styles.container} behavior="padding">

        <StatusBar barStyle="light-content" />

        <ImageBackground
          source={getImageForWeather(weather)}
          style={styles.imageContainer}
          imageStyle={styles.image}>

          <View style={styles.detailsContainer}>

            <ActivityIndicator animating={loading} color="white" size="large" />
            {!loading && (
              <View>
                {error && (
                  <Text style={[styles.smallText, styles.textStyle]}>
                    😞 Could not load your city or weather. Please try again later...
                  </Text>
                )}
                {!error && (
                  <View>
                    <Text style={[styles.mediumText, styles.textStyle]}>
                      {getIconForWeather(weather)} Tp.Hồ Chí Minh
                    </Text>
                   
                    <Text style={[styles.largeText, styles.textStyle]}>
                      <Text style={[styles.smallText, styles.textStyle]}>
                         Current Temp:&nbsp;   
                      </Text> 
                      {`${currentTemp}°C`} 
                    </Text>

                    <Text style={[styles.largeText, styles.textStyle]}>
                      <Text style={[styles.smallText, styles.textStyle]}>
                         Current Humid:&nbsp;   
                      </Text> 
                      {`${currentHumid}°`}
                    </Text>

                    <Text style={[styles.largeText, styles.textStyle]}>
                      <Text style={[styles.largeText, styles.textStyle]}>
                        <Text style={[styles.smallText, styles.textStyle]}>
                           Next Temp:&nbsp;   
                        </Text> 
                        {`${nextTemp}°C`}
                        &nbsp;&nbsp;   
                      </Text>
                    </Text>
                </View>
              )}

              <SearchInput 
                    placeholder="input Temp"
                    onSubmit = {(text) => this.setState({inputTemp:text})}
                    />
              <SearchInput 
                    placeholder="input Humid"
                    onSubmit = { (text) => this.setState({inputHumid:text})}
              /> 
              <Button  style={styles.buttonPadding}
                  onPress={this.handleUpdateLocation}
                  title="Learn More"
                  color="#841584"
                  accessibilityLabel="Learn more about this purple button"/>
              
              {!error && (
                <Text style={[styles.smallText, styles.textStyle]}>
                </Text>
              )}
            </View>
            )}
        </View>
        </ImageBackground>
      </KeyboardAvoidingView>
    );
  }
}

/* StyleSheet */
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#34495E',
  },
  imageContainer: {
    flex: 1,
  },
  image: {
    flex: 1,
    width: null,
    height: null,
    resizeMode: 'cover',
  },
  detailsContainer: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: 'rgba(0,0,0,0.2)',
    paddingHorizontal: 5
  },
  buttonPadding: {
    marginTop: 20
  },
  textStyle: {
    textAlign: 'center',
    fontFamily: Platform.OS === 'ios' ? 'AvenirNext-Regular' : 'Roboto',
    color: 'white',
  },
  largeText: {
    fontSize: 40,
  },
  mediumText:{
    fontSize: 27,
  },
  smallText: {
    fontSize: 15,
  },
});
