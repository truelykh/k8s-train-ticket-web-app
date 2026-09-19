package cancel.service;

import edu.fudan.common.entity.NotifyInfo;
import edu.fudan.common.entity.Order;
import edu.fudan.common.entity.User;
import edu.fudan.common.util.Response;
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

@RunWith(JUnit4.class)
public class CancelServiceImplTest {

    @InjectMocks
    private CancelServiceImpl cancelServiceImpl;

    @Mock
    private RestTemplate restTemplate;

    private HttpHeaders headers = new HttpHeaders();
    private HttpEntity requestEntity = new HttpEntity(headers);

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testCancelOrder1() {
        Order order = new Order();
        order.setStatus(6);
        Response<Order> response = new Response<>(1, null, order);
        ResponseEntity<Response<Order>> re = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class))).thenReturn(re);
        Response result = cancelServiceImpl.cancelOrder("order_id", "login_id", headers);
        Assert.assertEquals(new Response<>(0, "Order Status Cancel Not Permitted", null), result);
    }

    @Test
    public void testCancelOrder2() {
        Response<Order> response = new Response<>(0, null, null);
        ResponseEntity<Response<Order>> re = new ResponseEntity<>(response, HttpStatus.OK);
        Order order = new Order();
        order.setStatus(6);
        Response<Order> response2 = new Response<>(1, null, order);
        ResponseEntity<Response<Order>> re2 = new ResponseEntity<>(response2, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re).thenReturn(re2);
        Response result = cancelServiceImpl.cancelOrder("order_id", "login_id", headers);
        Assert.assertEquals(new Response<>(0, "Order Status Cancel Not Permitted", null), result);
    }

    @Test
    public void testSendEmail() {
        NotifyInfo notifyInfo = new NotifyInfo();
        ResponseEntity<Boolean> re = new ResponseEntity<>(true, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.POST),
                Mockito.any(HttpEntity.class),
                Mockito.eq(Boolean.class))).thenReturn(re);
        Boolean result = cancelServiceImpl.sendEmail(notifyInfo, headers);
        Assert.assertTrue(result);
    }

    @Test
    public void testCalculateRefund1() {
        Order order = new Order();
        order.setStatus(6);
        Response<Order> response = new Response<>(1, null, order);
        ResponseEntity<Response<Order>> re = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class))).thenReturn(re);
        Response result = cancelServiceImpl.calculateRefund("order_id", headers);
        Assert.assertEquals(new Response<>(0, "Order Status Cancel Not Permitted, Refound error", null), result);
    }

    @Test
    public void testCalculateRefund2() {
        Response<Order> response = new Response<>(0, null, null);
        ResponseEntity<Response<Order>> re = new ResponseEntity<>(response, HttpStatus.OK);
        Order order = new Order();
        order.setStatus(6);
        Response<Order> response2 = new Response<>(1, null, order);
        ResponseEntity<Response<Order>> re2 = new ResponseEntity<>(response2, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.any(HttpMethod.class),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class)))
                .thenReturn(re).thenReturn(re2);
        Response result = cancelServiceImpl.calculateRefund("order_id", headers);
        Assert.assertEquals(new Response<>(0, "Order Status Cancel Not Permitted", null), result);
    }

    @Test
    public void testDrawbackMoney() {
        Response response = new Response<>(1, null, null);
        ResponseEntity<Response> re = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.GET),
                Mockito.any(HttpEntity.class),
                Mockito.eq(Response.class))).thenReturn(re);
        Boolean result = cancelServiceImpl.drawbackMoney("money", "userId", headers);
        Assert.assertTrue(result);
    }

    @Test
    public void testGetAccount() {
        Response<User> response = new Response<>();
        ResponseEntity<Response<User>> re = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                Mockito.anyString(),
                Mockito.eq(HttpMethod.GET),
                Mockito.any(HttpEntity.class),
                Mockito.any(ParameterizedTypeReference.class))).thenReturn(re);
        Response<User> result = cancelServiceImpl.getAccount("orderId", headers);
        Assert.assertEquals(new Response<User>(null, null, null), result);
    }

}
