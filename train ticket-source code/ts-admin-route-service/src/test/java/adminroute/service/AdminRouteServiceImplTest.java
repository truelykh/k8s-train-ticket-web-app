package adminroute.service;

import edu.fudan.common.entity.Route;
import edu.fudan.common.entity.RouteInfo;
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

import java.util.HashMap;

@RunWith(JUnit4.class)
public class AdminRouteServiceImplTest {

    @InjectMocks
    private AdminRouteServiceImpl adminRouteServiceImpl;

    @Mock
    private RestTemplate restTemplate;

    private HttpHeaders headers = new HttpHeaders();
    private HttpEntity requestEntity = new HttpEntity(null);
    private Response response = new Response();
    private ResponseEntity<Response> re = new ResponseEntity<>(response, HttpStatus.OK);

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testGetAllRoutes() {
        Mockito.when(restTemplate.exchange(
                "http://ts-route-service/api/v1/routeservice/routes",
                HttpMethod.GET,
                requestEntity,
                Response.class)).thenReturn(re);
        Response result = adminRouteServiceImpl.getAllRoutes(headers);
        Assert.assertEquals(new Response<>(null, null, null), result);
    }

    @Test
    public void testCreateAndModifyRoute() {
        RouteInfo request = new RouteInfo();
        request.setStartStation("start_station");
        request.setEndStation("end_station");
        request.setStationList("start_station,end_station");
        request.setDistanceList("1,2");
        HttpEntity requestEntity2 = new HttpEntity(request, null);
        ResponseEntity<Response<Route>> re2 = new ResponseEntity<>(response, HttpStatus.OK);
        Mockito.when(restTemplate.exchange(
                "http://ts-station-service/api/v1/stationservice/stations/idlist",
                HttpMethod.POST,
                new HttpEntity(request.getStations(), null),
                Response.class)).thenReturn(new ResponseEntity<>(
                        new Response<>(1, "check stations Exist succeed", new HashMap<String, String>()), HttpStatus.OK));
        Mockito.when(restTemplate.exchange(
                "http://ts-route-service/api/v1/routeservice/routes",
                HttpMethod.POST,
                requestEntity2,
                new ParameterizedTypeReference<Response<Route>>() {
                })).thenReturn(re2);
        Response result = adminRouteServiceImpl.createAndModifyRoute(request, headers);
        Assert.assertEquals(new Response<>(null, null, null), result);
    }

    @Test
    public void testDeleteRoute() {
        Mockito.when(restTemplate.exchange(
                "http://ts-route-service/api/v1/routeservice/routes/" + "routeId",
                HttpMethod.DELETE,
                requestEntity,
                Response.class)).thenReturn(re);
        Response result = adminRouteServiceImpl.deleteRoute("routeId", headers);
        Assert.assertEquals(new Response<>(null, null, null), result);
    }

}
