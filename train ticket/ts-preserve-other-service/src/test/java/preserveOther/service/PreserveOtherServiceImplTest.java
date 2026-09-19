package preserveOther.service;

import edu.fudan.common.util.Response;
import edu.fudan.common.util.StringUtils;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import edu.fudan.common.entity.*;

import java.util.Date;
import java.util.HashMap;
import java.util.UUID;

@RunWith(JUnit4.class)
public class PreserveOtherServiceImplTest {

    @InjectMocks
    private PreserveOtherServiceImpl preserveOtherServiceImpl;

    @Mock
    private RestTemplate restTemplate;

    @Mock
    private preserveOther.mq.RabbitSend sendService;

    private HttpHeaders headers = new HttpHeaders();
    private HttpEntity requestEntity = new HttpEntity(headers);

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testPreserve() {
        OrderTicketsInfo oti = OrderTicketsInfo.builder()
                .accountId(UUID.randomUUID().toString())
                .contactsId(UUID.randomUUID().toString())
                .from("from_station")
                .to("to_station")
                .date(StringUtils.Date2String(new Date()))
                .handleDate("handle_date")
                .tripId("G1255")
                .seatType(2)
                .assurance(1)
                .foodType(1)
                .foodName("food_name")
                .foodPrice(1.0)
                .stationName("station_name")
                .storeName("store_name")
                .consigneeName("consignee_name")
                .consigneePhone("123456789")
                .consigneeWeight(1.0)
                .isWithin(true)
                .build();

        //response for checkSecurity()、createFoodOrder()、createConsign()
        Response response1 = new Response<>(1, null, null);
        ResponseEntity<Response> re1 = new ResponseEntity<>(response1, HttpStatus.OK);

        //response for sendEmail()
        ResponseEntity<Boolean> re10 = new ResponseEntity<>(true, HttpStatus.OK);

        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(Class.class)))
                .thenReturn(re1).thenReturn(re1).thenReturn(re1).thenReturn(re10);


        //response for getContactsById()
        Contacts contacts = new Contacts();
        contacts.setDocumentNumber("document_number");
        contacts.setName("name");
        contacts.setDocumentType(1);
        Response<Contacts> response2 = new Response<>(1, null, contacts);
        ResponseEntity<Response<Contacts>> re2 = new ResponseEntity<>(response2, HttpStatus.OK);

        //response for getTripAllDetailInformation()
        TripResponse tripResponse = new TripResponse();
        tripResponse.setConfortClass(1);
        tripResponse.setStartTime(StringUtils.Date2String(new Date()));
        TripAllDetail tripAllDetail = new TripAllDetail(true, "message", tripResponse, new Trip());
        Response<TripAllDetail> response3 = new Response<>(1, null, tripAllDetail);
        ResponseEntity<Response<TripAllDetail>> re3 = new ResponseEntity<>(response3, HttpStatus.OK);

        //response for queryForStationId()
        Response<String> response4 = new Response<>(1, null, "");
        ResponseEntity<Response<String>> re4 = new ResponseEntity<>(response4, HttpStatus.OK);

        //response for travel result
        TravelResult travelResult = new TravelResult();
        travelResult.setPrices( new java.util.HashMap<String, String>(){{ put("confortClass", "1.0"); put("economyClass", "1.0"); }} );
        edu.fudan.common.entity.Route route = new edu.fudan.common.entity.Route();
        route.setStations(new java.util.ArrayList<>());
        travelResult.setRoute(route);
        edu.fudan.common.entity.TrainType trainType = new edu.fudan.common.entity.TrainType();
        trainType.setConfortClass(100);
        trainType.setEconomyClass(100);
        travelResult.setTrainType(trainType);
        Response<TravelResult> response5 = new Response<>(1, null, travelResult);
        ResponseEntity<Response<TravelResult>> re5 = new ResponseEntity<>(response5, HttpStatus.OK);

        //response for dipatchSeat()
        Ticket ticket = new Ticket();
        ticket.setSeatNo(1);
        Response<Ticket> response6 = new Response<>(1, null, ticket);
        ResponseEntity<Response<Ticket>> re6 = new ResponseEntity<>(response6, HttpStatus.OK);

        //response for createOrder()
        Order order = new Order();
        order.setId(UUID.randomUUID().toString());
        order.setAccountId(UUID.randomUUID().toString());
        order.setTravelDate(StringUtils.Date2String(new Date()));
        order.setFrom("from_station");
        order.setTo("to_station");
        Response<Order> response7 = new Response<>(1, null, order);
        ResponseEntity<Response<Order>> re7 = new ResponseEntity<>(response7, HttpStatus.OK);

        //response for addAssuranceForOrder()
        Response<Assurance> response8 = new Response<>(1, null, null);
        ResponseEntity<Response<Assurance>> re8 = new ResponseEntity<>(response8, HttpStatus.OK);

        //response for getAccount()
        User user = new User();
        user.setEmail("email");
        user.setUserName("user_name");
        Response<User> response9 = new Response<>(1, null, user);
        ResponseEntity<Response<User>> re9 = new ResponseEntity<>(response9, HttpStatus.OK);

        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("contactservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re2);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("travel2service"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re3);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("seatservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re6);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("orderOtherService"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re7);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("userservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re9);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("basicservice"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re5);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.contains("assurance"),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re8);

        Response result = preserveOtherServiceImpl.preserve(oti, headers);
        Assert.assertEquals(new Response<>(1, "Success.", null), result);
    }

    @Test
    public void testDipatchSeat() {
        long mills = System.currentTimeMillis();
        Seat seatRequest = new Seat(StringUtils.Date2String(new Date()), "G1234", "start_station", "dest_station", 2, 100, null);
        HttpEntity requestEntityTicket = new HttpEntity<>(seatRequest, headers);
        Response<Ticket> response = new Response<>();
        ResponseEntity<Response<Ticket>> reTicket = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.anyString(),
                org.mockito.ArgumentMatchers.eq(HttpMethod.POST),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(reTicket);
        Ticket result = preserveOtherServiceImpl.dipatchSeat(StringUtils.Date2String(new Date()), "G1234", "start_station", "dest_station", 2, 100, null, headers);
        Assert.assertNull(result);
    }

    @Test
    public void testSendEmail() {
        NotifyInfo notifyInfo = new NotifyInfo();
        HttpEntity requestEntitySendEmail = new HttpEntity<>(notifyInfo, headers);
        ResponseEntity<Boolean> reSendEmail = new ResponseEntity<>(true, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                "http://ts-notification-service:17853/api/v1/notifyservice/notification/preserve_success",
                HttpMethod.POST,
                requestEntitySendEmail,
                Boolean.class)).thenReturn(reSendEmail);
        boolean result = preserveOtherServiceImpl.sendEmail(notifyInfo, headers);
        Assert.assertTrue(result);
    }

    @Test
    public void testGetAccount() {
        Response<User> response = new Response<>();
        ResponseEntity<Response<User>> re = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                org.mockito.ArgumentMatchers.anyString(),
                org.mockito.ArgumentMatchers.eq(HttpMethod.GET),
                org.mockito.ArgumentMatchers.any(org.springframework.http.HttpEntity.class),
                org.mockito.ArgumentMatchers.any(org.springframework.core.ParameterizedTypeReference.class)))
                .thenReturn(re);
        User result = preserveOtherServiceImpl.getAccount("1", headers);
        Assert.assertNull(result);
    }

}
